
      SUBROUTINE VAPORRESIST
C     
      IMPLICIT REAL*8(A-H,O-Z)
      DIMENSION A(10),B(10),C(10),CS(10),FKG(10),H(10),HS(10)
      DIMENSION HVAP(10),HWINIT(10),SMW(10),NAME(10),RHO(10)
      DIMENSION RHOW(10),U(10),W(10),X(10),YA(10),YB(10)
      DIMENSION XMOL(10),TBETA(10),PHI(10)
      CHARACTER*80 TITLE
      CHARACTER*16 INFILE,OUTFILE
      CHARACTER*25 NAME
      INTEGER NSOLV
C      
      COMMON/PRESSURE/ PTOT
      COMMON/SYPRIME/ W,X,H,WTOT,RHOW,CPS,RHOS,HWINIT,HINIT,
     $     TINIT,THICKWEB,SPHEAT,TU,TL,HU,HL,TW,VIEWW,HS,OLZONE,NSOLV
      COMMON/SHUMID/ WPOLY,DENSOL,U
      COMMON/SSOLV/ A,B,C,CS,FKG,HVAP,SMW,RHO,NAME
      COMMON/SRKFCONST/ B21,B31,B32,B41,B42,B43,B51,B52,B53,
     $     B54,B61,B62,B63,B64,B65,A1,A3,A4,A5,R1,R3,R4,R5,R6
      COMMON/EQUATIONS/ NEQNS
      COMMON/SPPEOS/ XMOL,TBETA,PHI
C     
C     * Disply selection to standard out
      WRITE(6,*)
      WRITE(6,2001)
2001  FORMAT(' VAPOR RESISTANCE DRYING MODEL')
      WRITE(6,*)
C      
C     ************************************************************
C     *           Infile data section: vapor.inp                 *
C     ************************************************************
C     * Opens data infiles and outfile
      INFILE ='vapor.inp'
      OUTFILE='vapor.out'
C      
      OPEN (UNIT=22,STATUS='OLD',FILE=INFILE)
      OPEN (UNIT=23,FILE=OUTFILE)
      OPEN (UNIT=24,FILE='vapor.csv') 
C      
C     * Write down model used
      WRITE(23,*) 'VAPOR RESISTANCE DRYING MODEL'
C      
C     * Reads line 1 of data file INFILE which is the run title
      READ(22,*)
      READ(22,500,ERR=4701) TITLE
      WRITE(23,501) TITLE
C      
C     * Reads line 2 of data file INFILE which is the web speed
C     *   and the coating width
      READ(22,*)
      READ(22,*,ERR=4702) WSPEED, CWIDTH, RATEMAX, NODES
C      
C     * Reads line 3 of data file INFILE which is the number
C     *   of solvent
      READ(22,*)
      READ(22,*,ERR=4703) NSOLV
      NEQNS = NSOLV+1
C     
C     * Write out headers for .csv file
      WRITE(24,101) 
      WRITE(24,102) ('SOLVENT',I,I=1,NSOLV)
C      
C     ************************************************************
C     *          Commented out for DME implementation            *
C     ************************************************************
C    * Reads line 4 of data file INFILE which is the solvent names
C      READ(22,*)
C      DO I = 1,NSOLV
C         READ(22,138,ERR=4704) NAME(I)
C         WRITE(*,*) 'NAME=',I, NAME(I)
C      END DO
C      
C     * Obtains solvent data
C      CALL VRSOLV (NSOLV)
C     ************************************************************
C      
C     ************************************************************
C     *          Added for DME implementation                    *
C     ************************************************************
C     * Reads solvent properties from new input file, solvent.inp
      OPEN (UNIT=20,STATUS='OLD',FILE='solvent.inp')
C
      DO I = 1,NSOLV
         READ(20,138) NAME(I)
         READ(20,*) A(I),B(I),C(I)
         READ(20,*) CS(I),FKG(I),HVAP(I),SMW(I),RHO(I)
         READ(20,*) TBETA(I),PHI(I)
C     * Convert Cal/gm to Btu/lb
         HVAP(I) = HVAP(I)*1.8D0
C     * Convert g/mol to lb/mol
         SMW(I) = 0.0022046D0*SMW(I)
C     * Convert gm/cc to lb/cuft
         RHO(I) = 62.4D0*RHO(I)
      END DO
C
      CLOSE(UNIT=20)
C     ************************************************************
C
C     * Generate constants for RKF subroutine
      CALL RKFCONST         
C      
C     * Reads line 4 of data file INFILE which is the mass 
C     *   fraction of the solvents and polymer and the solvent 
C     *   Flory-Huggins interaction parameter
      READ(22,*)
      READ(22,*,ERR=4705) (X(I),I=1,NSOLV+1),(U(I),I=1,NSOLV)
C      
C     * Reads line 5 of data file INFILE which is the initial 
C     *   web temp, weight of backing and solids, average heat 
C     *   capacity of backing and solids, total initial weight of 
C     *   coating
      READ(22,*)
      READ(22,*)
      READ(22,*,ERR=4706) T,DENSOL,SPHEAT,THICKWEB,RHOS,CPS,WTOT
      DENSOL = 62.4D0*DENSOL
      RHOS = 62.4D0*RHOS
C      
C     * Convert cm to ft
      THICKWEB = THICKWEB*0.03821D0
C     
C     * Convert T in deg C to deg F
      T = 1.8D0*T+32.0D0
      TINIT = T
C      
C     * Convert the weight of solids only from gm/sqm to lb/sqft
      WPOLY = X(NSOLV+1)*WTOT/4882.67D0
C      
C     * Total initial weight of solvents and polymer converted 
C     *   to lbs/sqft
      WTOT = WTOT/4882.67D0
C      
      VOLSOLV = 0.0D0
C      
C     * Unit area is specified to be 1 sqft
      AREA = 1.0D0
C     * Total pressure is 1 atmosphere 
      PTOT = 1.0D0
C
C     * Read line 7 repeatedly for the total number of drying 
C     *   sections
      READ(22,*)
      READ(22,*,ERR=4707) NZ
C      
C     * VOLSOLV in ft
      DO 4 I = 1,NSOLV
         VOLSOLV = VOLSOLV + X(I)*WTOT/RHO(I)
 4    CONTINUE
C      
C     * VOLTOT in ft and HINIT in ft (for unit area of media) 
      VOLTOT = VOLSOLV + WPOLY/DENSOL
      HINIT = VOLTOT/AREA
      WINITIAL = 0.0D0
C      
C     * W(I) in lb/sqft
      DO 3 I = 1,NSOLV
         W(I) = X(I)*WTOT/VOLTOT*HINIT
         HWINIT(I) = W(I)
         WINITIAL = WINITIAL + HWINIT(I)
 3    CONTINUE
C      
C     * Prints solvents used
      DO 13 I = 1,NSOLV
         WRITE(6,502) I,NAME(I)
         WRITE(23,502) I,NAME(I)
 13   CONTINUE
C      
C     * Convert gm/sqm to lb/sqft
      WRITE(6,503) WSPEED,CWIDTH,WTOT*4882.67D0
      WRITE(23,503) WSPEED,CWIDTH,WTOT*4882.67D0
C      
      IZONE = 0
      SUMT = 0.0D0
      ORATE = 0.0D0
      RTIMEOLD = 0.0D0
      RATEOLD = 0.0D0
C      
C     ************************************************************
C     * Loop 5 is continued until the number of zones is         * 
C     *   completed                                              *         
C     ************************************************************
      READ(22,*)
      READ(22,*)
      READ(22,*)
C      
      DO 5 I = 1,NZ
C         
C     * Reads line 8 of data file INFILE which is the oven air 
C     *   temps and htcs
         READ(22,*,ERR=4708) TU,HU,TL,HL
         
C     * Converts convective heat transfer coefficient from 
C     *   Cal/sqm/s/C to Btu/sqft/min/F
         HU = HU/1.355D0/60.0D0
         HL = HL/1.355D0/60.0D0
C         
C     * Reads line 9 of data file INFILE which is wall temperature, 
C     *   air humidities, maximum time step, print distance, zone 
C     *   length
	 READ(22,*,ERR=4709) TW,VIEWW,(HS(J),J=1,NSOLV),
     $        HMAX,PDIST,OLZONE
C         
C     * Print the headings for dryer section
         WRITE(23,197) I,TU,HU*1.355D0*60.0D0,TL,HL*1.355D0*60.0D0
         WRITE(23,*)
         WRITE(23,208) TW,VIEWW
         WRITE(23,*)
C
	 DO 202 J = 1,NSOLV
            WRITE(23,201) J,HS(J)
 202     CONTINUE
C     
C     * Write out headers for .out file
         WRITE(23,103) 
         WRITE(23,104) ('SOLVENT',I,I=1,NSOLV)
C     
C     * Convert metric to english units
C     * deg C to deg R
         TW = (TW*1.8D0+32.0D0)+460.0D0
C     * deg C to deg F
         TU = TU*1.8D0+32.0D0
         TL = TL*1.8D0+32.0D0
C
C     ************************************************************
C     * Starting time step, minimum and maximum time step in     *
C     *   minutes, print increment and total number of print     *
C     *   intervals.                                             *
C     ************************************************************
         TOL = 1.0D-3
         HSTART = 1.0D-6
         HMIN = 1.0D-14
C
C     * Change the maximum time step sizes in different iterations
C     HMAX=HMAX/DFLOAT(2**(ITER-1))
C     WRITE(*,*) 'MAXIMUM TIME STEP SIZE =',HMAX  

C     * Change the tolerance in different iterations
C     TOL = TOL/DFLOAT(2**(ITER-1))
C     IF (I .EQ. 1) WRITE(*,*) 'RELATIVE TOLERANCE =',TOL

C     * Change the initial time step size
C     HSTART=HSTART/DFLOAT(2**(ITER-1))
C     IF (I .EQ. 1) WRITE(*,*) 'INITIAL STEP SIZE =',HSTART
         DELT = PDIST/WSPEED
C
         IF (INT(OLZONE/PDIST) .LT. OLZONE/PDIST) THEN
            NINCR = INT(OLZONE/PDIST)+1
         ELSE
            NINCR = INT(OLZONE/PDIST)
         ENDIF
C
         IZONE = IZONE+1
C
         RATEMOLD = 0.0D0
         DO 9 J = 1,NSOLV
            RATEMOLD = RATEMOLD+W(J)
 9       CONTINUE
C     
C     ************************************************************
C     *            Start of numerical integration                *
C     ************************************************************
C     * Print initial data
C     * JP is a dummy variable to tell when the iterations are 
C     *   greater than 2 which is compared in the print subroutine
           JP = 0 
C
         YA(NSOLV+1) = T
         DO 10 J = 1,NSOLV
            YA(J) = W(J)
 10      CONTINUE
         B2 = 0.0D0
C
         CALL VRPRINT (JP,IZONE,RATEOLD,SUMT,T,W,WPOLY,NSOLV,B2,
     $        WINITIAL,WSPEED,RATEMAX,NSTEP)
C         
C     * Loop to solve the differential equations
         DO 100 J = 1,NINCR
C     * Starting time value of interval
	    A2 = (J-1)*DELT
C     * Stopping time value of interval 
	    B2 = J*DELT
C
C     * RKF differential equation solver
	    CALL DESOLV (A2,B2,YA,TOL,HSTART,HMIN,HMAX,YB,IFLAG)
C     
	    T = YB(NSOLV+1)
	    DO 110 K = 1,NSOLV
               W(K) = YB(K)
 110        CONTINUE
C     
            CALL VRPRINT (JP,IZONE,RATEOLD,SUMT,T,W,WPOLY,NSOLV,
     $           B2,WINITIAL,WSPEED,RATEMAX,NSTEP)
            IF (IFLAG .EQ. 0) THEN
               WRITE(*,*) 'ERROR: TIME STEP SIZE TOO SMALL'
               STOP
            ENDIF
C      
C     * Update starting value of Y's
	    DO 127 K = 1,NEQNS
               YA(K) = YB(K)     
 127        CONTINUE
C     
 100     CONTINUE
C     
         TOTMASS = 0.0D00
         DO 130 K = 1,NSOLV
	    TOTMASS = TOTMASS + W(K)
 130     CONTINUE
C     
C     * Convert from lb/sqft to gm/sqm
         ORATE = ((RATEMOLD-TOTMASS)/(SUMT-RTIMEOLD))*4882.67D0*
     $        CWIDTH/100.0D0*OLZONE*60.0D0
         WRITE(23,210) I,ORATE
         RTIMEOLD = SUMT
C     
C     * Repeat the complete process if more than 1 dryer zone is used
 5    CONTINUE
C     
      CLOSE(UNIT=22)
      CLOSE(UNIT=23)
      CLOSE(UNIT=24)
C     
      RETURN
C     
C     * Data format statements
 101  FORMAT(1X,'DISTANCE,',5X,'TIME,',9X,'TEMP,',9X,'PERCENT,',
     $     6X,'RATE,',9X,'SOLVENT REMAINING,',/,1X,'cm,',
     $     11X,'sec,',10X,'deg C,',8X,'REMAINING,',
     $     4X,'gm/sqm/min,',3X,'gm/sqm,')
 102  FORMAT(10X,',',4(13X,','),3(4X,A7,I2,','))
 103  FORMAT(1X,'DISTANCE',5X,'TIME',9X,'TEMP',9X,'PERCENT',
     $     6X,'RATE',9X,'SOLVENT REMAINING',/,1X,'cm',
     $     11X,'sec',10X,'deg C',8X,'REMAINING',
     $     4X,'gm/sqm/min',3X,'gm/sqm')
 104  FORMAT(10X,4(13X),4X,3(A7,I2,3X))
 138  FORMAT(A25)
 197  FORMAT(/,' DRYING SECTION ',I3,//,
     $     '        TU = ',E12.4E3,' deg C',7X,
     $     'HU  = ',E12.4E3,' Cal/sqm/sec/deg C',/,
     $     '        TL = ',E12.4E3,' deg C',7X,
     $     'HL  = ',E12.4E3,' Cal/sqm/sec/deg C')
 201  FORMAT(' OVEN PARTIAL PRESSURE OF SOLVENT ',I2,' IS ',E12.4E3,
     $     ' atm',//)
 204  FORMAT(/,' INPUT NAME OF FILE FOR OUTPUT',/)
 206  FORMAT(/,' INPUT NAME OF FILE WITH OVEN DATA',/)
 207  FORMAT(A16)
 208  FORMAT('     TWALL = ',E12.4E3,' deg C',6x,'VIEW = ',E12.4E3)
 210  FORMAT(/,' THE OVERALL DRYING RATE IN DRYING SECTION ',I2,
     $     ' IS ',E12.4E3,' gm/min',/)
 500  FORMAT(A80)
 501  FORMAT(/,1X,A80/)
 502  FORMAT(' SOLVENT ',I2,' IS ',A25)
 503  FORMAT(/,' THE WSPEED IS ',E12.4E3,' meters/min',/,
     $     ' THE CWIDTH IS ',E12.4E3,' cm',/,
     $     ' THE WTOT   IS ',E12.4E3,' gm/sqm')
C 
C     * Error handling
 4701 WRITE(6,*)' ERROR READING TITLE'
      STOP
 4702 WRITE(6,*)' ERROR READING WEB SPEED AND COATING WIDTH'
      STOP
 4703 WRITE(6,*)' ERROR READING NUMBER OF SOLVENTS'
      STOP
 4704 WRITE(6,*)' ERROR READING NAME OF SOLVENTS'
      STOP
 4705 WRITE(6,*)' ERROR READING WT FRACTIONS AND FLORY PARAMETERS'
      STOP
 4706 WRITE(6,*)' ERROR READING WEB AND SOLIDS INPUT DATA'
      STOP
 4707 WRITE(6,*)' ERROR READING NUMBER OF ZONES'
      STOP
 4708 WRITE(6,*)' ERROR READING ZONE AIR TEMPERATURES AND HTCS'
      STOP
 4709 WRITE(6,*)' ERROR READING WALL TEMP, AIR CONC, INTEGRATION DATA'
      STOP     
C
      END





















