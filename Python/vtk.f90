!------------------------------------------------------------------------------
! The Vtk output solver begins here
!------------------------------------------------------------------------------
MODULE VtkLegacyFile

    USE MeshUtils
    USE ElementDescription
 
    IMPLICIT NONE
!   PRIVATE
    SAVE

    PUBLIC :: WriteVtkLegacyFile

    TYPE :: VtkCell_t
        INTEGER :: nNodes
        ! FIXME: POINTER -> ALLOCATABLE when more compilers support it
        INTEGER, POINTER :: NodeIndex(:)
    END TYPE VtkCell_t

    INTEGER, PARAMETER :: VtkUnit = 58


CONTAINS

    SUBROUTINE WriteVtkLegacyFile( VtkFile, Model, SubtractDisp )
        CHARACTER(LEN=*), INTENT(IN) :: VtkFile
        TYPE(Model_t) :: Model 
        LOGICAL, INTENT(IN) :: SubtractDisp
        TYPE(Variable_t), POINTER :: Var,Var1
        CHARACTER(LEN=512) :: str
        !LOGICAL :: FreeSurfaceFlag
        INTEGER :: i,j,k

        OPEN( UNIT=VtkUnit, FILE=VtkFile, STATUS='UNKNOWN' )

        !FreeSurfaceFlag = FreeSurface( Model )

        CALL WriteGrid( VtkUnit, Model, SubtractDisp )

        WRITE( VtkUnit,'("POINT_DATA ",I0)' ) Model % NumberOfNodes

        Var => Model % Variables
        DO WHILE( ASSOCIATED( Var ) )
            IF ( .NOT.Var % Output ) THEN
                Var => Var % Next
                CYCLE
            END IF

            SELECT CASE( Var % Name )
            CASE( 'time','timestep','timestep size', 'timestep interval' )

            CASE( 'mesh update' )
                Var1 => Model % Variables

                DO WHILE( ASSOCIATED( Var1 ) )
                    IF ( TRIM( Var1 % Name ) == 'displacement' ) EXIT
                    Var1 => Var1 % Next
                END DO

                IF ( .NOT.ASSOCIATED( Var1 ) ) THEN
                    CALL WriteVector("Mesh.Update", Var, Model % NumberOfNodes,&
                                     3, VtkUnit)
                END IF

            CASE( 'mesh update 1','mesh update 2', 'mesh update 3' )

            CASE( 'displacement' )
                WRITE( VtkUnit,'("VECTORS ",A," double")' ) "Displacement"
                DO i = 1, Model % NumberOfNodes
                    k = i
                    IF ( ASSOCIATED( Var % Perm ) ) k = Var % Perm(k)

                    IF ( k > 0 ) THEN
                        DO j=1,Var % DOFs
                            WRITE( VtkUnit,'(E20.11E3)',ADVANCE='NO' ) &
                                            Var % Values(Var % DOFs*(k-1)+j)
                        END DO
                        IF ( Var % DOFs < 3 ) THEN
                            WRITE( VtkUnit,'(" 0.0")',ADVANCE='NO' )
                        END IF
                        WRITE( VtkUnit, * ) 
                    ELSE
                        Var1 => Model % Variables
                        DO WHILE( ASSOCIATED( Var1 ) )
                            IF ( TRIM( Var1 % Name ) == 'mesh update' ) EXIT
                            Var1 => Var1 % Next
                        END DO
                        IF ( ASSOCIATED( Var1 ) ) THEN
                            k = i
                            IF ( ASSOCIATED(Var1 % Perm ) ) k = Var1 % Perm(k)
                            IF ( k > 0 ) THEN
                                DO j=1,Var1 % DOFs
                                    WRITE( VtkUnit,'(E20.11E3)',ADVANCE='NO' ) &
                                          Var1 % Values(Var1 % DOFs*(k-1)+j)
                                END DO
                                IF ( Var1 % DOFs < 3 ) THEN
                                    WRITE( VtkUnit,'(" 0.0")', ADVANCE='NO' )
                                END IF
                                WRITE( VtkUnit, * ) 
                            ELSE
                                WRITE( VtkUnit,'(" 0.0 0.0 0.0")' )
                            END IF
                        ELSE
                            WRITE( VtkUnit,'(" 0.0 0.0 0.0")' )
                        END IF
                    END IF
                END DO

            CASE( 'displacement 1','displacement 2','displacement 3' )

            CASE( 'flow solution' )
                CALL WriteVector( "Velocity", Var, Model % NumberOfNodes, 4, &
                                  VtkUnit )
                WRITE( VtkUnit,'("SCALARS ",A," double")' ) "Pressure"
                WRITE( VtkUnit,'("LOOKUP_TABLE default")' )
                DO i = 1, Model % NumberOfNodes
                    k = i
                    IF ( ASSOCIATED( Var % Perm ) ) k = Var % Perm(k)
                    WRITE( VtkUnit,'(E20.11E3)' ) &
                                       Var % Values(Var % DOFs*(k-1)+Var % DOFs)
                END DO

            CASE( 'velocity 1','velocity 2','velocity 3','pressure' )

            CASE( 'magnetic field' )
                CALL WriteVector( "MagField", Var, Model % NumberOfNodes, 3, &
                                  VtkUnit)
            CASE( 'magnetic field 1','magnetic field 2', 'magnetic field 3' )

            CASE( 'electric current' )
                CALL WriteVector( "Current", Var, Model % NumberOfNodes, 3, &
                                  VtkUnit)
            CASE('electric current 1','electric current 2','electric current 3')

            CASE( 'coordinate 1','coordinate 2','coordinate 3' )

            CASE( 'magnetic flux density' )
                CALL WriteVector("MagneticFlux", Var, Model % NumberOfNodes, 3,&
                                 VtkUnit)
            CASE( 'magnetic flux density 1','magnetic flux density 2', &
                  'magnetic flux density 3' )

            CASE DEFAULT
                IF ( Var % DOFs == 1 ) THEN
                    DO i=1,Var % NameLen
                        str(i:i) = Var % Name(i:i)
                        IF (str(i:i) == ' ') str(i:i) = '.'
                    END DO
                    str(1:1) = CHAR(ICHAR(str(1:1))-ICHAR('a')+ICHAR('A'))

                    WRITE(VtkUnit,'("SCALARS ",A," double")') str(1:Var%NameLen)
                    WRITE( VtkUnit,'("LOOKUP_TABLE default")' )
                    DO i = 1, Model % NumberOfNodes
                        k = i
                        IF ( ASSOCIATED( Var % Perm ) ) k = Var % Perm(k)
                        IF ( k > 0 ) THEN
                            WRITE( VtkUnit,'(E20.11E3)' ) Var % Values(k)
                        ELSE
                            WRITE( VtkUnit,'(" 0.0")' )
                        END IF
                    END DO
                END IF
            END SELECT
            Var => Var % Next
        END DO

!        IF ( FreeSurfaceFlag ) THEN
!            WRITE( VtkUnit,'("VECTORS ",A," double")' ) "Coordinates"
!
!            DO i = 1, Model % NumberOfNodes
!                Var => VariableGet( Model % Variables,'Coordinate 1' )
!                WRITE( VtkUnit,'(E20.11E3)',ADVANCE='NO' ) Var % Values(i)
!
!                Var => VariableGet( Model % Variables, 'Coordinate 2' )
!                WRITE( VtkUnit,'(E20.11E3)',ADVANCE='NO' ) Var % Values(i)
!
!                Var => VariableGet( Model % Variables, 'Coordinate 3' )
!                WRITE( VtkUnit,'(E20.11E3)' ) Var % Values(i)
!            END DO
!        END IF

        CLOSE( VtkUnit )
    END SUBROUTINE WriteVtkLegacyFile


    SUBROUTINE WriteVector( VarName, Var, nNodes, MaxDOF, IOUnit )
        CHARACTER(*), INTENT(IN) :: VarName
        TYPE(Variable_t), INTENT(IN) :: Var
        INTEGER, INTENT(IN) :: nNodes, MaxDOF, IOUnit
        INTEGER :: i, j, k, n

        n = Var % DOFs - (MaxDOF - 3)

        WRITE( IOUnit, '("VECTORS ",A," double")' ) TRIM( VarName )
        DO i = 1, nNodes
            k = i
            IF ( ASSOCIATED( Var % Perm ) ) k = Var % Perm(k)
            IF ( k > 0 ) THEN
                DO j=1, n
                    WRITE( IOUnit,'(E20.11E3)',ADVANCE='NO' ) &
                                    Var % Values(Var % DOFs*(k-1)+j)
                END DO
                IF ( n < 3 ) THEN
                    WRITE( IOUnit,'(" 0.0")',ADVANCE='NO' )
                END IF
                WRITE( IOUnit, * ) 
            ELSE
                WRITE( IOUnit,'(" 0.0 0.0 0.0")' )
            END IF
        END DO
    END SUBROUTINE WriteVector


    LOGICAL FUNCTION FreeSurface( Model )
        TYPE(Model_t), INTENT(IN) :: Model
        LOGICAL :: MoveBoundary, GotIt
        INTEGER :: i

        FreeSurface = .FALSE.
        MoveBoundary = .FALSE.
        DO i = 1, Model % NumberOfBCs
            FreeSurface = FreeSurface &
                       .OR. ListGetLogical( Model % BCs(i) % Values, &
                                            'Free Surface', GotIt )
            IF ( FreeSurface ) THEN
                MoveBoundary = ListGetLogical( Model % BCs(i) % Values, &
                                               'Internal Move Boundary', GotIt )
         
                IF ( .NOT.GotIt ) MoveBoundary = .TRUE.

                FreeSurface = FreeSurface .AND. MoveBoundary
            END IF

            IF ( FreeSurface ) EXIT
        END DO
    END FUNCTION FreeSurface


    SUBROUTINE WriteGrid ( IOUnit, Model, SubtractDisp )
        INTEGER, INTENT(IN) :: IOUnit
        TYPE(Model_t), INTENT(IN) :: Model
        LOGICAL, INTENT(IN) :: SubtractDisp ! Subtract Displacement from Coords.
        TYPE(Variable_t), POINTER :: Displacement, MeshUpdate, Var1, Var2
        INTEGER :: i, k, l, nVtkCells, nVtkCellNum
        ! FIXME: POINTER -> ALLOCATABLE when more compilers support it
        TYPE(VtkCell_t), POINTER :: VtkCells(:)

        WRITE ( IOUnit, '("# vtk DataFile Version 3.0")' ) 
        WRITE ( IOUnit, '("ElmerSolver output; started at ", A)' ) TRIM( FormatDate() )
        WRITE ( IOUnit, '("ASCII")' ) 
        WRITE ( IOUnit, '("DATASET UNSTRUCTURED_GRID")' ) 

        !
        ! Coordinates: 
        !
        WRITE ( IOUnit, '("POINTS ", I0, " double")' ) Model % NumberOfNodes

        ! First, look for displacements
        Displacement => NULL()
        MeshUpdate => NULL()
        IF ( SubtractDisp ) THEN
            Var1 => Model % Variables
            DO WHILE( ASSOCIATED( Var1 ) )
                IF ( .NOT.Var1 % Output ) THEN
                    Var1 => Var1 % Next
                    CYCLE
                END IF

                SELECT CASE( Var1 % Name )
                CASE( 'mesh update' )
                    Var2 => Model % Variables
                    DO WHILE( ASSOCIATED( Var2 ) )
                        IF ( TRIM( Var2 % Name ) == 'displacement' ) EXIT
                        Var2 => Var2 % Next
                    END DO

                    IF ( .NOT. ASSOCIATED( Var2 ) ) THEN
                        Displacement => Var1
                    ELSE
                        MeshUpdate   => Var1
                    END IF

                CASE( 'displacement' )
                    Displacement => Var1
                END SELECT

                Var1 => Var1 % Next
            END DO
        END IF

        DO i = 1, Model % NumberOfNodes
            IF ( .NOT.ASSOCIATED( Displacement ) ) THEN
                WRITE( IOUnit,'(3E20.11E3)' ) Model % Nodes % x(i), &
                                              Model % Nodes % y(i), &
                                            Model % Nodes % z(i)
                CYCLE
            END IF

            k = Displacement % Perm(i)
            l = 0
            IF ( ASSOCIATED( MeshUpdate ) ) l = MeshUpdate % Perm(i)

            IF ( k > 0 ) THEN
                k = Displacement % DOFs * (k-1)
                SELECT CASE( Displacement % DOFs )
                CASE(1)
                    WRITE( IOUnit,'(3E20.11E3)' ) &
                            Model % Nodes % x(i) - Displacement % Values(k+1), &
                            Model % Nodes % y(i), &
                            Model % Nodes % z(i)
                CASE( 2 )
                    WRITE( IOUnit,'(3E20.11E3)' ) &
                            Model % Nodes % x(i) - Displacement % Values(k+1), &
                            Model % Nodes % y(i) - Displacement % Values(k+2), &
                            Model % Nodes % z(i)
                CASE(3)
                    WRITE( IOUnit,'(3E20.11E3)' ) &
                            Model % Nodes % x(i) - Displacement % Values(k+1), &
                            Model % Nodes % y(i) - Displacement % Values(k+2), &
                            Model % Nodes % z(i) - Displacement % Values(k+3)
                END SELECT
            ELSE IF ( l > 0 ) THEN
                k = MeshUpdate % DOFs * (l-1)
                SELECT CASE( MeshUpdate % DOFs )
                CASE(1)
                    WRITE( IOUnit,'(3E20.11E3)' ) &
                            Model % Nodes % x(i) - MeshUpdate % Values(k+1), &
                            Model % Nodes % y(i), &
                            Model % Nodes % z(i)
                CASE(2)
                    WRITE( IOUnit,'(3E20.11E3)' ) &
                            Model % Nodes % x(i) - MeshUpdate % Values(k+1), &
                            Model % Nodes % y(i) - MeshUpdate % Values(k+2), &
                            Model % Nodes % z(i)
                CASE(3)
                    WRITE( IOUnit,'(3E20.11E3)' ) &
                            Model % Nodes % x(i) - MeshUpdate % Values(k+1), &
                            Model % Nodes % y(i) - MeshUpdate % Values(k+2), &
                            Model % Nodes % z(i) - MeshUpdate % Values(k+3)
                END SELECT
            ELSE
                WRITE( IOUnit,'(3E20.11E3)' ) Model % Nodes % x(i), &
                                            Model % Nodes % y(i), &
                                            Model % Nodes % z(i)
            ENDIF
        END DO

        WRITE ( IOUnit, * )

        !
        ! CELLS
        !
        CALL GetNVtkCells ( Model, nVtkCells, nVtkCellNum )
        
        WRITE( IOUnit,'("CELLS ",I0," ",I0)' ) nVtkCells, nVtkCellNum
        DO i = 1, Model%NumberOfBulkElements + Model%NumberOfBoundaryElements

            CALL Elements2Cells ( Model % Elements(i), VtkCells )

            DO k = 1, SIZE( VtkCells )
                WRITE( IOUnit, '(I0)', ADVANCE='NO' ) VtkCells(k) % nNodes
                WRITE( IOUnit, '(50(" ",I0))') VtkCells(k) % NodeIndex
                DEALLOCATE( VtkCells(k) % NodeIndex )
            END DO

            ! FIXME: These explicit deallocations of VtkCells(j) % NodeIndex and
            ! VtkCells can be removed if/when they are changed to ALLOCATABLEs
            DEALLOCATE ( VtkCells )

        END DO

        WRITE( IOUnit, * )

        !
        ! CELL_TYPES
        !
        WRITE( IOUnit,'("CELL_TYPES ",I0)' ) nVtkCells
        DO i = 1, Model%NumberOfBulkElements + Model%NumberOfBoundaryElements
            CALL WriteCellType ( IOUnit, Model%Elements(i)%TYPE%ElementCode )
        END DO

        WRITE( IOUnit, * )

    CONTAINS

        ! Here's a bunch of routines to deal with ELMER Element -> VTK Cell
        ! translations.   Most element types has a directly corresponding cell
        ! type, but some have to be expanded to a compound of simplier cell
        ! types.

        ! nVtkCells is the number of VtkCells, and VtkCellNum is the total
        ! number of integer numbers we have to write to the 'CELLS' section.

        SUBROUTINE GetNVtkCells( Model,nVtkCells,nVtkCellNum )
            TYPE(Model_t), INTENT(IN) :: Model
            INTEGER, INTENT(OUT) :: nVtkCells, nVtkCellNum

            nVtkCells = 0
            nVtkCellNum = 0
            DO i = 1, Model%NumberOfBulkElements+Model%NumberOfBoundaryElements
                SELECT CASE ( Model % Elements(i) % TYPE % ElementCode )
                CASE( 409 )
                    ! Translate to 4 VTK_QUAD cells
                    nVtkCells = nVtkCells + 4
                    nVtkCellNum = nVtkCellNum + 16 + 4

                CASE DEFAULT
                    nVtkCells = nVtkCells + 1
                    nVtkCellNum = nVtkCellNum &
                                + Model % Elements(i) % TYPE % NumberOfNodes + 1
                END SELECT
            END DO
        END SUBROUTINE GetNVtkCells


        ! Translate an Element_t to an array of VtkCell_t.

        SUBROUTINE Elements2Cells( Elem, VtkCells )
            TYPE(Element_t), INTENT(IN) :: Elem
            ! FIXME: POINTER -> ALLOCATABLE, INTENT(OUT) when more compilers
            ! support it
            TYPE(VtkCell_t), POINTER :: VtkCells(:)
            INTEGER :: k

            SELECT CASE ( Elem % TYPE % ElementCode )
            CASE( 409 )
                ! Translate to 4 VTK_QUAD cells
                ALLOCATE( VtkCells(4) )

                VtkCells % nNodes = 4
                DO k = 1, 4
                    ALLOCATE( VtkCells(k) % NodeIndex(4) )
                END DO
                VtkCells(1) % NodeIndex = (/ Elem % NodeIndexes(1), &
                                             Elem % NodeIndexes(5), &
                                             Elem % NodeIndexes(9), &
                                             Elem % NodeIndexes(8) /) - 1
                VtkCells(2) % NodeIndex = (/ Elem % NodeIndexes(5), &
                                               Elem % NodeIndexes(2), &
                                               Elem % NodeIndexes(6), &
                                               Elem % NodeIndexes(9) /) - 1
                VtkCells(3) % NodeIndex = (/ Elem % NodeIndexes(9), &
                                               Elem % NodeIndexes(6), &
                                               Elem % NodeIndexes(3), &
                                               Elem % NodeIndexes(7) /) - 1
                VtkCells(4) % NodeIndex = (/ Elem % NodeIndexes(8), &
                                               Elem % NodeIndexes(9), &
                                               Elem % NodeIndexes(7), &
                                               Elem % NodeIndexes(4) /) - 1
            CASE DEFAULT
                ALLOCATE( VtkCells(1) )

                VtkCells % nNodes = Elem % TYPE % NumberOfNodes
                ALLOCATE( VtkCells(1) % NodeIndex(VtkCells(1) % nNodes) )
                VtkCells(1) % NodeIndex = Elem % NodeIndexes-1
            END SELECT

        END SUBROUTINE Elements2Cells


        SUBROUTINE WriteCellType( IOUnit,Code )
            INTEGER, INTENT(IN) :: IOUnit, Code

            SELECT CASE (Code)
            CASE( 101 )
                WRITE( IOUnit,'(I0)' ) 1
            CASE( 202 )
                WRITE( IOUnit,'(I0)' ) 3
            CASE( 203 )
                WRITE( IOUnit,'(I0)' ) 21
            CASE( 303 )
                WRITE( IOUnit,'(I0)' ) 5
            CASE( 306 )
                WRITE( IOUnit,'(I0)' ) 22
            CASE( 404 )
                WRITE( IOUnit,'(I0)' ) 9
            CASE( 408 )
                WRITE( IOUnit,'(I0)' ) 23
            CASE( 409 )
                ! Translate to 4 VTK_QUAD cells
                WRITE( IOUnit,'(I0)' ) (/ 9, 9, 9, 9 /)
            CASE( 504 )
                WRITE( IOUnit,'(I0)' ) 10
            CASE( 510 )
                WRITE( IOUnit,'(I0)' ) 24
            CASE( 605 )
                WRITE( IOUnit,'(I0)' ) 14
            CASE( 706 )
                WRITE( IOUnit,'(I0)' ) 13
            CASE( 808 )
                WRITE( IOUnit,'(I0)' ) 12
            CASE( 820 )
                WRITE( IOUnit,'(I0)' ) 25
            CASE DEFAULT
                WRITE( IOUnit,'(I0)' ) -Code
            END SELECT
        END SUBROUTINE WriteCellType

    END SUBROUTINE WriteGrid

END MODULE VtkLegacyFile


!------------------------------------------------------------------------------
SUBROUTINE VtkOutputSolver( Model,Solver,dt,TransientSimulation )
!DEC$ATTRIBUTES DLLEXPORT :: VtkOutputSolver
!------------------------------------------------------------------------------

    USE DefUtils 
    USE VtkLegacyFile

    IMPLICIT NONE
    TYPE(Solver_t) :: Solver
    TYPE(Model_t) :: Model
    REAL(dp) :: dt
    LOGICAL :: TransientSimulation

    INTEGER, SAVE :: nTime = 0
    LOGICAL :: GotIt
    CHARACTER(MAX_NAME_LEN), SAVE :: FilePrefix

    ! Avoid compiler warings about unused variables
    IF ( TransientSimulation ) THEN; ENDIF
    IF ( dt > 0.0 ) THEN; ENDIF

    IF ( nTime == 0 ) THEN
      FilePrefix = GetString( Solver % Values,'Output File Name',GotIt )
      IF ( .NOT.GotIt ) FilePrefix = "Output"
    END IF
    nTime = nTime + 1

    CALL WriteData( TRIM(FilePrefix), Model, nTime )


CONTAINS

    SUBROUTINE WriteData( Prefix, Model, nTime )
        CHARACTER(*), INTENT(IN) :: Prefix
        TYPE(Model_t) :: Model
        INTEGER, INTENT(IN) :: nTime
        CHARACTER(MAX_NAME_LEN) :: VtkFile
        TYPE(Mesh_t), POINTER :: Mesh
        TYPE(Variable_t), POINTER :: Var
        INTEGER :: i, j, k
        LOGICAL :: EigAnal
        REAL(dp), POINTER :: OrigValues(:)
        INTEGER :: OrigDOFs
        CHARACTER(MAX_NAME_LEN) :: Dir

        Mesh => Model % Meshes
        DO WHILE( ASSOCIATED(Mesh) )
            IF ( .NOT.Mesh % OutputActive ) THEN
                Mesh => Mesh % next
                CYCLE
            END IF

            IF (LEN_TRIM(Mesh % Name) > 0 ) THEN
                Dir = TRIM(Mesh % Name) // "/"
            ELSE
                Dir = "./"
            END IF

            CALL SetCurrentMesh( Model, Mesh )

            EigAnal = .FALSE.

   Solvers: DO i = 1, Model % NumberOfSolvers
                EigAnal = ListGetLogical( Model % Solvers(i) % Values, &
                                          "Eigen Analysis", GotIt )
                Var => Model % Solvers(i) % Variable
                IF ( EigAnal .AND. ASSOCIATED(Var % EigenValues) ) THEN
                    DO j = 1, Model % Solvers(i) % NOfEigenValues
                        OrigValues => Var % Values
                        OrigDOFs = Var % DOFs

                        IF ( Model % Solvers(i) % Matrix % COMPLEX ) THEN
                            Var % DOFs = Var % DOFs*2
                            ALLOCATE( Var % Values(2*SIZE(Var%EigenVectors,2)) )
                            FORALL ( k = 1:SIZE(Var % Values)/2 )
                                Var%Values(2*k-1) = REAL(Var%EigenVectors(j,k))
                                Var%Values(2*k) = AIMAG(Var%EigenVectors(j,k))
                            END FORALL
                        ELSE
                            ALLOCATE( Var % Values(SIZE(Var % EigenVectors,2)) )
                            Var % Values = Var % EigenVectors(j,:)
                        END IF

                        WRITE( VtkFile, '(A,A,I4.4,"_",I2.2,".vtk")' ) &
                                         TRIM(Dir), Prefix, nTime, j
                        CALL WriteVtkLegacyFile( VtkFile, Model, .FALSE. )

                        DEALLOCATE( Var % Values )
                        Var % Values => OrigValues
                        Var % DOFs = OrigDOFs
                    END DO
                    EXIT Solvers
                END IF
            END DO Solvers

            IF ( .NOT.EigAnal ) THEN
                WRITE( VtkFile,'(A,A,I4.4,".vtk")' ) TRIM(Dir),Prefix,nTime
                CALL WriteVtkLegacyFile( VtkFile, Model, .TRUE. )
            END IF

            Mesh => Mesh % next
        END DO
    END SUBROUTINE WriteData

END SUBROUTINE VtkOutputSolver
