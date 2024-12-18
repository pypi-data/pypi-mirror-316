///////////////////////////////////////////////////////////////////////////////
// Description: This file contains the class declaration for                 //
// BBarFourNodeQuadUP, a 4-node plane strain element for solid-fluid fully   //
// coupled analysis. This implementation is a simplified u-p formulation     //
// of Biot theory (u - solid displacement, p - fluid pressure).              //
// Each element node has two DOFs for u and 1 DOF for p.                     //
// Constant volume/pressure integration (BBar method) is used for integration//
// of the volumetric component of solid phase and the fulid phase.           //
//                                                                           //
// Written by Zhaohui Yang    (June 2009)                                    //
///////////////////////////////////////////////////////////////////////////////
//
// Date: 2009-10-07 20:02:23
//
#ifndef BBarFourNodeQuadUP_h
#define BBarFourNodeQuadUP_h

#ifndef _bool_h
#include <stdbool.h>
#endif

#include <Element.h>
#include <Matrix.h>
#include <Vector.h>
#include <ID.h>
#include <quadrature/Plane/LegendreFixedQuadrilateral.h>

class Node;
class NDMaterial;
class Response;

class BBarFourNodeQuadUP : public Element,
                           protected LegendreFixedQuadrilateral<4>
{
  public:

    BBarFourNodeQuadUP(int tag, int nd1, int nd2, int nd3, int nd4,
                       NDMaterial &m, const char *type,
                       double t, double bulk, double rhof, double perm1, double perm2,
                       double b1 = 0.0, double b2 = 0.0, double p = 0.0);

    BBarFourNodeQuadUP();
    virtual ~BBarFourNodeQuadUP();

    const char *getClassType() const {return "BBarFourNodeQuadUP";};
    static constexpr const char* class_name = "BBarFourNodeQuadUP";
    int getNumExternalNodes() const;
    const ID &getExternalNodes();
    Node **getNodePtrs();

    int getNumDOF();
    void setDomain(Domain *theDomain);

    // public methods to set the state of the element
    int commitState();
    int revertToLastCommit();
    int revertToStart();
    int update();

    // public methods to obtain stiffness, mass, damping and residual information
    const Matrix &getTangentStiff();
    const Matrix &getInitialStiff();
    const Matrix &getDamp();
    const Matrix &getMass();

    void zeroLoad();
    int addLoad(ElementalLoad *theLoad, double loadFactor);
    int addInertiaLoadToUnbalance(const Vector &accel);
    const Vector &getResistingForce();
    const Vector &getResistingForceIncInertia();

    // public methods for element output
    int sendSelf(int commitTag, Channel &theChannel);
    int recvSelf(int commitTag, Channel &theChannel, FEM_ObjectBroker
          &theBroker);
    int displaySelf(Renderer &, int mode, float fact, const char **displayModes=0, int numModes=0);
    void Print(OPS_Stream &s, int flag =0);

    Response *setResponse(const char **argv, int argc, OPS_Stream &s);
    int getResponse(int responseID, Information &eleInformation);
    int setParameter(const char **argv, int argc, Parameter &param);
    int updateParameter(int parameterID, Information &info);

    // RWB; PyLiq1 & TzLiq1 need to see the excess pore pressure and initial stresses.
    friend class PyLiq1;
    friend class TzLiq1;
    friend class QzLiq1; // Sumeet

  protected:

  private:
    // private member functions - only objects of this class can call these
    double mixtureRho(int ipt);  // Mixture mass density at integration point i
    void shapeFunction();
    void setPressureLoadAtNodes();

    constexpr static int NEN = 4; // number of nodes;
    constexpr static int NDM = 2; // number of dimensions
    constexpr static int NDF = 3; // number of DOFs per node

    // private attributes - a copy for each object of the class
    NDMaterial **theMaterial; // pointer to the ND material objects
    ID connectedExternalNodes; // Tags of quad nodes


    Vector Q;        // Applied nodal loads
    double b[2];        // Body forces

    double appliedB[2]; // Body forces applied with load pattern, C.McGann, U.Washington
    int applyLoad;      // flag for body force in load, C.McGann, U.Washington
    
    Vector pressureLoad;    // Pressure load at nodes

    double thickness;    // Element thickness
    double rho;            // Fluid mass per unit volume
    double kc;             // combined bulk modulus
    double pressure;       // Normal surface traction (pressure) over entire element

    // Note: positive for outward normal
    double perm[2];  // lateral/vertical permeability

    // [0,1=derivative wrt x, y; 2=shape func][node][Gauss point]
    static double shp[3][4][4];    // Stores shape functions and derivatives (overwritten)
//  static double pts[4][2];    // Stores quadrature points
//  static double wts[4];        // Stores quadrature weights
    static double dvol[4];  // Stores detJacobian (overwritten)

    // [x,y][node]
    static double shpBar[2][4]; // Stores averaged shap functions (overwritten)

    // [row][col][node][Gauss point]
    static double B[4][2][4][4];  // Stores strain-displacement matrix (overwritten)

    // [col][node][Gauss point]  Note: there is only one row in Bp matrix
    static double Bp[2][4][4]; // Stores strain-displacement matrix for fluid phase (overwritten)

    Matrix *Ki;
    static Matrix K;        // Element stiffness, damping, and mass Matrix
    static Vector P;        // Element resisting force vector

    static Node *theNodes[NEN];
    Node *nd1Ptr;               // Pointers to quad nodes
    Node *nd2Ptr;
    Node *nd3Ptr;
    Node *nd4Ptr;
};

#endif
