! Script “tx2nc.F”
      PROGRAM tx2nc
c     gfortran -I$NCDFINC tx2nc.F -L$NCDFLIB -lnetcdf -lnetcdff -o tx2nc.x
      IMPLICIT NONE
      include "netcdf.inc"

      INTEGER nx, ny, nt, n
!      PARAMETER (nx=30, ny=30, nt=312, n=1201) ! all stations
!      PARAMETER (nx=30, ny=30, nt=312, n=1014) ! stations with > 10 years data
!      PARAMETER (nx=30, ny=30, nt=312, n=511) ! stations with > 20 years data
      PARAMETER (nx=30, ny=30, nt=323, n=511) ! stations with > 20 years data

      REAL aodin(n,nt),aodfin(n,nt)
      REAL aod(nx,ny,nt), aodf(nx,ny,nt)
      REAL naod(nx,ny,nt), naodf(nx,ny,nt)
      INTEGER ncid, aodid, aodfid, xid, yid, tid
      INTEGER xdim(1), ydim(1), tdim(1)
      INTEGER x1id, y1id
      INTEGER start(3), count(3), dims(3)
      INTEGER start2(2), count2(2), dims2(2)
      INTEGER i,j,l,k,ierr
      INTEGER ll, l1
      REAL xx,yy
      REAL x(nx,ny), y(nx,ny), time(nt)
      REAL x1(nx), y1(ny)
      REAL miss
      PARAMETER (miss=-999.)
      CHARACTER*50 station

      aod(:,:,:) = 0.
      aodf(:,:,:) = 0.
      naod(:,:,:) = 0.
      naodf(:,:,:) = 0.

      OPEN(1,file='stations')
      DO k = 1,n
         READ(1,*) station
         OPEN(2,file='stations.txt/'//station)
         READ(2,'(i6)') ll
         READ(2,'(f9.6)') xx
         READ(2,'(f9.6)') yy
         DO l=1,ll
            READ(2,'(2f12.6)') aodin(k,l),aodfin(k,l)
         ENDDO
         CLOSE(2)
         i = NINT((180.+xx)/12.)+1
         j = NINT((90.-yy)/6.)+1
         write(*,*) station,xx,yy,i,j,ll
         l1=0
         DO l=nt-ll,nt
            l1=l1+1
            IF (aodin(k,l1).GT.0.) THEN
               aod(i,j,l) = aod(i,j,l)+aodin(k,l1)
               naod(i,j,l) = naod(i,j,l) + 1.
            ENDIF
            IF (aodfin(k,l1).GT.0.) THEN
               aodf(i,j,l) = aodf(i,j,l)+aodfin(k,l1)
               naodf(i,j,l) = naodf(i,j,l) + 1.
            ENDIF
         ENDDO
      ENDDO
      CLOSE(1)
      DO i=1,nx
         DO j=1,ny
            DO l=1,nt
               IF ( naod(i,j,l).GT.0. ) THEN
                  aod(i,j,l) = aod(i,j,l) / naod(i,j,l)
               ELSE
                  aod(i,j,l) = miss
               ENDIF
               IF ( naodf(i,j,l).GT.0. ) THEN
                  aodf(i,j,l) = aodf(i,j,l) / naodf(i,j,l)
               ELSE
                  aodf(i,j,l) = miss
               ENDIF
            ENDDO
         ENDDO
      ENDDO

      start(1:3)=1
      count(1)=nx
      count(2)=ny
      count(3)=nt
      start2(1:2)=1
      count2(1)=nx
      count2(2)=ny
      DO i=1,nx
         x(i,:)=FLOAT(i-1)*12-174.
         x1(i)=x(i,1)
      ENDDO
      DO j=1,ny
         y(:,j)=87.-FLOAT(j-1)*6.
         y1(j)=y(1,j)
      ENDDO
      DO l=1,nt
         time(l)=FLOAT(l)
      ENDDO
      !ncid = NCCRE ('aeronet.nc', NCCLOB, ierr)
      ncid = NCCRE ('aeronet_10yrs.nc', NCCLOB, ierr)
      IF (ierr.NE.NF_NOERR) STOP 'error creating file'
      ierr = NF_DEF_DIM(ncid, 'lon', nx, xdim)
      IF (ierr.NE.NF_NOERR) STOP 'create x d'
      ierr = NF_DEF_DIM(ncid, 'lat', ny, ydim)
      IF (ierr.NE.NF_NOERR) STOP 'create y d'
      ierr = NF_DEF_DIM(ncid, 'time', nt, tdim)
      IF (ierr.NE.NF_NOERR) STOP 'create t d'
      dims(1)=xdim(1)
      dims(2)=ydim(1)
      dims(3)=tdim(1)
      dims2(1)=xdim(1)
      dims2(2)=ydim(1)
      ierr = NF_DEF_VAR (ncid, 'xlon', NF_FLOAT, 2, dims2, xid)
      IF (ierr.NE.NF_NOERR) STOP 'def xlon'
      ierr = NF_PUT_ATT_TEXT(ncid, xid, 'units', 9, 'degrees_E')
      IF (ierr.NE.NF_NOERR) STOP 'error def units'
      ierr = NF_DEF_VAR (ncid, 'ylat', NF_FLOAT, 2, dims2, yid)
      IF (ierr.NE.NF_NOERR) STOP 'def ylat'
      ierr = NF_DEF_VAR (ncid, 'lon', NF_FLOAT, 1, xdim, x1id)
      IF (ierr.NE.NF_NOERR) STOP 'def lon'
      ierr = NF_PUT_ATT_TEXT(ncid, x1id, 'units', 9, 'degrees_E')
      IF (ierr.NE.NF_NOERR) STOP 'error def units'
      ierr = NF_DEF_VAR (ncid, 'lat', NF_FLOAT, 1, ydim, y1id)
      IF (ierr.NE.NF_NOERR) STOP 'def lat'
      ierr = NF_PUT_ATT_TEXT(ncid, y1id, 'units', 9, 'degrees_N')
      IF (ierr.NE.NF_NOERR) STOP 'error def units'
      ierr = NF_DEF_VAR (ncid, 'time', NF_FLOAT, 1, tdim, tid)
      IF (ierr.NE.NF_NOERR) STOP 'def time'
      ierr = NF_PUT_ATT_TEXT(ncid, tid, 'units', 23,
     .     'months since 1993-12-15')
      IF (ierr.NE.NF_NOERR) STOP 'error def units'
      !
      ierr = NF_DEF_VAR (ncid, 'aod', NF_FLOAT, 3, dims, aodid)
      IF (ierr.NE.NF_NOERR) STOP 'def var'
      ierr = NF_PUT_ATT_REAL(ncid, aodid, 'missing_value',
     .     NF_FLOAT, 1, miss)
      IF (ierr.NE.NF_NOERR)  stop 'error def missing value'
      ierr = NF_DEF_VAR (ncid, 'aodf', NF_FLOAT, 3, dims, aodfid)
      IF (ierr.NE.NF_NOERR) STOP 'def var'
      ierr = NF_PUT_ATT_REAL(ncid, aodfid, 'missing_value',
     .     NF_FLOAT, 1, miss)
      IF (ierr.NE.NF_NOERR)  stop 'error def missing value'
      !
      ierr = NF_ENDDEF(ncid)
      IF (ierr.NE.NF_NOERR) STOP 'end def  .'
      !
      ierr = NF_PUT_VARA_REAL (ncid, yid, start2, count2, y)
      IF (ierr.NE.NF_NOERR) STOP 'write y var.'
      ierr = NF_PUT_VARA_REAL (ncid, xid, start2, count2, x)
      IF (ierr.NE.NF_NOERR) STOP 'write x var.'
      ierr = NF_PUT_VARA_REAL (ncid, y1id, start(2), count(2), y1)
      IF (ierr.NE.NF_NOERR) STOP 'write y1 var.'
      ierr = NF_PUT_VARA_REAL (ncid, x1id, start(1), count(1), x1)
      IF (ierr.NE.NF_NOERR) STOP 'write x1 var.'
      ierr = NF_PUT_VARA_REAL (ncid, tid, start(3), count(3), time)
      IF (ierr.NE.NF_NOERR) STOP 'write time var.'
      !
      ierr = NF_PUT_VARA_REAL (ncid, aodid, start, count, aod)
      IF (ierr.NE.NF_NOERR) STOP 'write aod var.'
      ierr = NF_PUT_VARA_REAL (ncid, aodfid, start, count, aodf)
      IF (ierr.NE.NF_NOERR) STOP 'write aodf var.'
      !
      ierr = NF_CLOSE(ncid)

      END PROGRAM tx2nc
