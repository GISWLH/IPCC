      PROGRAM aodtrend
c gfortran -I$NCDFINC aodtrend.F -L$NCDFLIB -lnetcdf -lnetcdff -o aodtrend.x
      IMPLICIT NONE
#include "netcdf.inc"
c
c      
      INTEGER nx,ny,nt       ! number of longitudes (nx), latitudes (ny), and time (nt)     
      PARAMETER (nx=30, ny=30, nt=20)
      
      REAL mi(nx,ny,nt), mo(nx,ny,nt) ! AOD from MISR (mi) MODIS (mo)
      REAL mif(nx,ny,nt), mof(nx,ny,nt) ! fine-mode AOD for mi, mo
      REAL mm(nx,ny,nt), mmf(nx,ny,nt)
      
      REAL m(nx,ny), mf(nx,ny)  ! mean values over time; MODIS is average over Terra and Aqua where overlapping
      REAL t(nx,ny), tf(nx,ny) ! trends 
      REAL s(nx,ny), sf(nx,ny) ! significance of trends
      REAL lon(nx),lat(ny) ! Longitude and latitude
      REAL miss ! missing value
      PARAMETER (miss=-9999.)

      INTEGER i,j,l,ll! loop indices

      INTEGER ncid              ! output fileid
      INTEGER dims(2)           ! output file dimensions
      INTEGER status

      CALL get(nx,ny,nt,lon,lat,mi,mo,mif,mof) ! call subroutine to read in NetCDF file
      
      DO i=1,nx
         DO j=1,ny
            DO l=1,nt
               IF ( mo(i,j,l).GT.0. .AND. mi(i,j,l).GT.0 ) THEN ! get MISR-MODIS average
                  mm(i,j,l) = 0.5*(mo(i,j,l)+mi(i,j,l))
               ELSE
                  mm(i,j,l) = -1. !MAX(mo(i,j,l),mi(i,j,l)) ! take the not-missing one
               ENDIF
               IF ( mof(i,j,l).GT.0. .AND. mif(i,j,l).GT.0 ) THEN ! get MISR-MODIS average
                  mmf(i,j,l) = 0.5*(mof(i,j,l)+mif(i,j,l))
               ELSE
                  mmf(i,j,l) = -1. ! MAX(mof(i,j,l),mif(i,j,l)) ! take the not-missing one
               ENDIF
            ENDDO
         ENDDO
      ENDDO
      CALL trend(nx,ny,nt,mm,m,t,s) ! for AOD
      CALL trend(nx,ny,nt,mmf,mf,tf,sf) ! same for AODFM

      CALL writehead(nx,ny,lon,lat,ncid,dims)
      CALL writevar(nx,ny,ncid,dims,'mm ',m,t,s)
      CALL writevar(nx,ny,ncid,dims,'mf ',mf,tf,sf)

      status = NF_CLOSE(ncid) 
      END PROGRAM aodtrend
c=======================================
      SUBROUTINE trend(
     i     nx,ny,nt,d,
     o     m,t,s)
      
      IMPLICIT NONE
      ! input
      INTEGER nx, ny, nt        ! dimensions
      REAL d(nx,ny,nt)          ! data

      ! output
      REAL m(nx,ny)             ! time-mean
      REAL t(nx,ny)             ! trend
      REAL s(nx,ny)             ! significance of trend

      ! for regression
      REAL a                    ! sum of data over time
      REAL ab                   ! sum of product time and AOD / AODFM
      REAL b                    ! sum over AOD / AODFM
      REAL b2                   ! square of AOD/AODFM
      REAL r                    ! Regression coefficient
      REAL n, reg_denom         ! number of timesteps, temporary variable
      
      ! for significance test
      REAL alpha(20)            ! values for 0.1 two-sided t-test, https://en.wikipedia.org/wiki/Student%27s_t-distribution#Table_of_selected_values
      DATA alpha/6.314,2.920,2.353,2.132,2.015,1.943,1.895,1.860,1.833,
     .     1.812,1.796,1.782,1.771,1.761,1.753,1.746,1.740,1.734,1.729,
     .     1.725/
      ! rest is from Santer et al. 2000 doi 10.1029/1999JD901105
      REAL sb                   ! standard error
      REAL se                   ! variance of regression residuals
      REAL r1                   ! lag-1 autocorrelation coefficient
      REAL var                  ! variance
      REAL ne                   ! effective sample size
      REAL dt                   ! quadratic deviation of time from mean
      REAL tb                   ! test quantity
      REAL miss ! missing value
      PARAMETER (miss=-9999.)

      ! loop indices
      INTEGER i,j,l,ll
      
      m = 0.                    ! initialize mean to zero
      
      DO j=1,ny
         DO i=1,nx
            a=0.                ! initialize regression parameters
            ab=0.
            b=0.
            b2=0.
            n=0.
            DO l=1,nt
               IF ( d(i,j,l).GT.0. ) THEN ! valid AOD/AODFM for positive values
                  n=n+1.        ! count for years
                  b=b+n         ! sum over years
                  b2=b2+n*n     ! sum of b^2
                 
                  a=a+d(i,j,l)  ! sum over data
                  ab=ab+n*d(i,j,l) ! sum of product
                  m(i,j) = m(i,j) + d(i,j,l) ! summing up data to obtain mean
               ENDIF
            ENDDO               ! time loop
            s(i,j) = 0.
            IF ( n.GT.10. ) THEN ! consider only grid points with enough data
               m(i,j) = m(i,j)/n ! compute mean
               reg_denom=n*b2-b*b ! regression coefficient denominator
               t(i,j) = (n*ab-a*b)/reg_denom/m(i,j)*100. ! relative regression coefficient in percent
               
               ! Regression equation:
               r = (n*ab-a*b)/reg_denom ! regression coefficient
               b = b/n          ! mean x value
               a = a/n          ! mean y valye
               a = a - b*r      ! intercept
               
               ! Compute autocorrelation coefficient, variance and rmse
               r1=0.
               var=0.
               se=0.
               dt=0.
               n=0.
               DO l=1,nt
                  IF ( d(i,j,l).GT.0. ) THEN ! valid AOD/AODFM for positive values
                     n=n+1.     ! count for years
                     IF ( l.LT.nt ) THEN
                        IF ( d(i,j,l+1).GT.0. ) THEN
                           r1=r1+(d(i,j,l)-m(i,j))*(d(i,j,l+1)-m(i,j)) ! autocorrelation
                        ENDIF
                     ENDIF
                     var=var+(d(i,j,l)-m(i,j))**2 ! variance
                     se=se + (d(i,j,l) - (a+r*(l)))**2 ! Santer Eq. 1/4
                     dt=dt+(l-b)**2 ! for Santer Eq. 3, denominator
                  ENDIF
               ENDDO
               r1=abs(r1/var) ! lag-1 autocorrelation coefficient
               ne = n*(1-r1)/(1+r1) ! Santer Eq. 6
               se = ( 1/(ne-2)*se )**0.5 ! Santer Eq. 4
               sb = se/(dt**0.5)  ! Santer Eq. 1
               tb = r / sb      ! Santer Eq. 5
               !write(*,*) r,tb,sb,se,r1,ne
               IF ( abs(tb).GT.alpha(INT(n)) ) THEN
                  s(i,j) = 0.1
               ENDIF
            ELSE
               t(i,j) = miss    ! if not enough data -> missing values
               m(i,j) = miss
            ENDIF
            !s(i,j) = abs(tb)
         ENDDO                  ! longitude loop
      ENDDO                     ! latitude loop
      END SUBROUTINE trend
            
      
c     
c=======================================
      
      SUBROUTINE get(
     i     nx,ny,nt,
     o     lon,lat,
     o     mi,mo,mif,mof)
      IMPLICIT NONE
c
c Read in data from a NetCDF-File
c
#include "netcdf.inc"
      !
      ! Input 
      INTEGER nx,ny,nt
      ! 
      ! Output
      REAL mi(nx,ny,nt), mo(nx,ny,nt)
      REAL mif(nx,ny,nt), mof(nx,ny,nt)
      REAL lon(nx), lat(ny)
      !
      ! Local
      INTEGER ierr, ncid, vid      
      INTEGER start(3), count(3)
      INTEGER i,j,l
      
      start(1:3)=1
      count(1)=nx
      count(2)=ny
      count(3)=nt

      ierr = NF_OPEN('misr_2000-2019_30x30.nc',NF_NOWRITE, ncid)
      IF (ierr.NE.NF_NOERR) stop 'Error in opening initial file'
      ierr = NF_INQ_VARID (ncid, 'Aerosol_Optical_Depth', vid)
      IF (ierr.NE.NF_NOERR)  stop 'error read var'
      ierr = NF_GET_VARA_REAL (ncid, vid, start, count, mi)      
      IF (ierr.NE.NF_NOERR)  stop 'error read mi data'
      ierr = NF_INQ_VARID (ncid, 'Small_Mode_Aerosol_Optical_Depth',
     .     vid)
      IF (ierr.NE.NF_NOERR)  stop 'error read var'
      ierr = NF_GET_VARA_REAL (ncid, vid, start, count, mif)      
      IF (ierr.NE.NF_NOERR)  stop 'error read mif data'
      ierr = NF_CLOSE(ncid)
      IF (ierr.NE.NF_NOERR) STOP 'pb close file'

      count(3)=18
      ierr = NF_OPEN('modis_2000-2019_30x30.nc',NF_NOWRITE, ncid)
      IF (ierr.NE.NF_NOERR) stop 'Error in opening initial file'
      ierr = NF_INQ_VARID (ncid, 'aod_landocean', vid)
      IF (ierr.NE.NF_NOERR)  stop 'error read var'
      ierr = NF_GET_VARA_REAL (ncid, vid, start, count, mo)      
      IF (ierr.NE.NF_NOERR)  stop 'error read ma data'
      ierr = NF_INQ_VARID (ncid, 'aod550_ocean_fm_qa', vid)
      IF (ierr.NE.NF_NOERR)  stop 'error read var'
      ierr = NF_GET_VARA_REAL (ncid, vid, start, count, mof)      
      IF (ierr.NE.NF_NOERR)  stop 'error read mat data'
      ierr = NF_INQ_VARID (ncid, 'lon', vid)
      IF (ierr.NE.NF_NOERR)  stop 'error read lon var'
      ierr = NF_GET_VARA_REAL (ncid, vid, start(1), count(1), lon)      
      IF (ierr.NE.NF_NOERR)  stop 'error read lon data'
      ierr = NF_INQ_VARID (ncid, 'lat', vid)
      IF (ierr.NE.NF_NOERR)  stop 'error read lat var'
      ierr = NF_GET_VARA_REAL (ncid, vid, start(2), count(2), lat)      
      IF (ierr.NE.NF_NOERR)  stop 'error read lat data'
      ierr = NF_CLOSE(ncid)
      IF (ierr.NE.NF_NOERR) STOP 'pb close file'

      DO i=1,nx
         DO j=1,ny
            mo(i,j,19) = -9999.
            mof(i,j,19) = -9999.
         ENDDO
      ENDDO
      
      RETURN
      END SUBROUTINE get
c===================================      
      SUBROUTINE writehead(
     i     nx,ny,rlon,rlat,
     o     ncid,dims)
      IMPLICIT NONE
#include "netcdf.inc"

      ! INput
      INTEGER nx,ny
      REAL rlon(nx), rlat(nx)

      INTEGER status, ncid
      CHARACTER*30 name, unit
      
      INTEGER londim(1), latdim(1)
      INTEGER lonid, latid
      INTEGER dims(2) ! Field containing the two dimensions
      
      ncid = NCCRE ('mimof.nc', NCCLOB, status)
      IF (status.NE.NF_NOERR)  stop 'error creating file'
      
      ! Define the dimensions:
      status = NF_DEF_DIM(ncid, 'lon', nx, londim)
      IF (status.NE.NF_NOERR)  stop 'error def lon'
      status = NF_DEF_DIM(ncid, 'lat', ny, latdim)
      IF (status.NE.NF_NOERR)  stop 'error def lat'

      ! define the axis variables
      status  = NF_DEF_VAR (ncid,'lon',NF_FLOAT,1,londim,lonid)
      IF (status.NE.NF_NOERR)  stop 'error def lonvar'
      status  = NF_DEF_VAR (ncid,'lat',NF_FLOAT,1,latdim,latid)
      IF (status.NE.NF_NOERR)  stop 'error def latvar'
      
      name = 'latitude' ! The variable description
      unit = 'degrees_N'! The unit
      ! The "8" is for 8 characters in the name ("latitude")
      status = NF_PUT_ATT_TEXT(ncid, latid, 'long_name', 8, name) 
      IF (status.NE.NF_NOERR)  stop 'error def lat att name'
      status = NF_PUT_ATT_TEXT(ncid, latid, 'units', 9, unit) 
      IF (status.NE.NF_NOERR)  stop 'error def lat att unit'

      name = 'longitude'
      unit = 'degrees_E'
      status = NF_PUT_ATT_TEXT(ncid, lonid, 'long_name', 9, name) 
      IF (status.NE.NF_NOERR)  stop 'error def lon att name'
      status = NF_PUT_ATT_TEXT(ncid, lonid, 'units', 9, unit) 
      IF (status.NE.NF_NOERR)  stop 'error def lon att unit'
      
      ! End of definitions:
      status = NF_ENDDEF(ncid)
      IF (status.NE.NF_NOERR)  stop 'error enddef '

      ! And now assign the values defined in section (0.)
      status = NF_PUT_VAR_REAL(ncid, lonid, rlon)
      IF (status.NE.NF_NOERR)  stop 'error write lon'
      status = NF_PUT_VAR_REAL(ncid, latid, rlat)
      IF (status.NE.NF_NOERR)  stop 'error write lat'

      dims(1)=londim(1) ! First dimension is longitude
      dims(2)=latdim(1) ! 2nd latitude
      
      RETURN 
      END SUBROUTINE writehead

c===================================      
      SUBROUTINE writevar(
     i     nx,ny,ncid,dims,
     i     id,
     i     m,t,s)
      IMPLICIT NONE
#include "netcdf.inc"

      ! Input
      INTEGER nx,ny
      INTEGER ncid, dims(2)
      CHARACTER*3 id
      REAL m(nx,ny), t(nx,ny), s(nx,ny)
      
      INTEGER status
      CHARACTER*30 name, unit

      INTEGER mid,tid,sid
      INTEGER start(2), count(2)
      REAL miss ! missing value
      PARAMETER (miss=-9999.)
      
      ! Re-start definitions in the NetCDF-file:
      status = NF_REDEF(ncid)
      IF (status.NE.NF_NOERR)  stop 'error restart def'      
      
      ! Define the variable in the file
      !                       name               #dims
      status = NF_DEF_VAR (ncid,'m'//id, NF_FLOAT,2,dims,mid)
      if (status.NE.NF_NOERR) stop 'err def m var'      
      status = NF_PUT_ATT_REAL(ncid, mid, 'missing_value', 
     .     NF_FLOAT, 1, miss)
      IF (status.NE.NF_NOERR)  stop 'error def missing value'
      status = NF_DEF_VAR (ncid,'t'//id, NF_FLOAT,2,dims,tid)
      if (status.NE.NF_NOERR) stop 'err def t var'      
      status = NF_PUT_ATT_REAL(ncid, tid, 'missing_value', 
     .     NF_FLOAT, 1, miss)
      status = NF_DEF_VAR (ncid,'s'//id, NF_FLOAT,2,dims,sid)
      if (status.NE.NF_NOERR) stop 'err def s var'      
      status = NF_PUT_ATT_REAL(ncid, sid, 'missing_value', 
     .     NF_FLOAT, 1, miss)
      IF (status.NE.NF_NOERR)  stop 'error def missing value'
      
      ! Done with definitions
      status = NF_ENDDEF(ncid)
      IF (status.NE.NF_NOERR)  stop 'error end def'
            
      start(1)=1
      start(2)=1
      count(1)=nx
      count(2)=ny
      
      ! Write the values
      status = NF_PUT_VARA_REAL(ncid, mid, start, count, m)      
      if (status.NE.NF_NOERR) stop 'err write m var'     
      status = NF_PUT_VARA_REAL(ncid, tid, start, count, t)      
      if (status.NE.NF_NOERR) stop 'err write t var'     
      status = NF_PUT_VARA_REAL(ncid, sid, start, count, s)      
      if (status.NE.NF_NOERR) stop 'err write s var'     

      RETURN
      END SUBROUTINE writevar
