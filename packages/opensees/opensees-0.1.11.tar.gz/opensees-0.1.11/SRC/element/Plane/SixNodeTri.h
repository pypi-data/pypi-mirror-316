/* ****************************************************************** **
**    OpenSees - Open System for Earthquake Engineering Simulation    **
**          Pacific Earthquake Engineering Research Center            **
**                                                                    **
**                                                                    **
** (C) Copyright 1999, The Regents of the University of California    **
** All Rights Reserved.                                               **
**                                                                    **
** Commercial use of this program without express permission of the   **
** University of California, Berkeley, is strictly prohibited.  See   **
** file 'COPYRIGHT'  in main directory for information on usage and   **
** redistribution,  and for a DISCLAIMER OF ALL WARRANTIES.           **
**                                                                    **
** Developed by:                                                      **
**   Frank McKenna (fmckenna@ce.berkeley.edu)                         **
**   Gregory L. Fenves (fenves@ce.berkeley.edu)                       **
**   Filip C. Filippou (filippou@ce.berkeley.edu)                     **
**                                                                    **
** ****************************************************************** */
//
// Description: This file contains the class definition for SixNodeTri.
//
// Written: Seweryn Kokot, Opole University of Technology, Poland
// Created: Sep 2020
//
// based on FourNodeQuad by MHS
//
#ifndef SixNodeTri_h
#define SixNodeTri_h

#include <stdbool.h>
#include <array>
#include <Element.h>
#include <ID.h>
#include <Matrix.h>
#include <Vector.h>

class Node;
class NDMaterial;
class Response;

class SixNodeTri : public Element {
public:
  SixNodeTri(int tag,
             const std::array<int,6> & nodes,
             NDMaterial &m, const char *type, double t,
             double pressure = 0.0, double rho = 0.0, double b1 = 0.0,
             double b2 = 0.0);
  SixNodeTri();
  ~SixNodeTri();

  const char *getClassType() const { return "SixNodeTri"; }

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
  const Matrix &getMass();

  void zeroLoad();
  int addLoad(ElementalLoad *theLoad, double loadFactor);
  int addInertiaLoadToUnbalance(const Vector &accel);

  const Vector &getResistingForce();
  const Vector &getResistingForceIncInertia();

  // public methods for element output
  int sendSelf(int commitTag, Channel &theChannel);
  int recvSelf(int commitTag, Channel &theChannel, FEM_ObjectBroker &theBroker);

  void Print(OPS_Stream &s, int flag = 0);

  Response *setResponse(const char **argv, int argc, OPS_Stream &s);

  int getResponse(int responseID, Information &eleInformation);

  int setParameter(const char **argv, int argc, Parameter &param);
  int updateParameter(int parameterID, Information &info);

  // RWB; PyLiq1 & TzLiq1 need to see the excess pore pressure and initial
  // stresses.
  friend class PyLiq1;
  friend class TzLiq1;
  friend class QzLiq1; // Sumeet

protected:
private:
  // private attributes

  static constexpr int nip = 3; // number of integration/Gauss points
  static constexpr int NEN = 6; // number of nodes
  static constexpr int NDM = 2;
  static constexpr int NDF = 2;

  std::array<NDMaterial *, nip> theMaterial; // pointer to the ND material objects

  ID connectedExternalNodes; // Tags of quad nodes

  std::array<Node *,NEN> theNodes;

  static double matrixData[(NEN*2)*(NEN*2)]; // array data for matrix
  static Matrix K;              // Element stiffness, damping, and mass Matrix
  static Vector P;              // Element resisting force vector
  Vector Q;                     // Applied nodal loads
  double b[2];                  // Body forces

  double appliedB[2]; // Body forces applied with load pattern, C.McGann,
                      // U.Washington
  int applyLoad;      // flag for body force in load, C.McGann, U.Washington

  Vector pressureLoad; // Pressure load at nodes

  double thickness; // Element thickness
  double pressure;  // Normal surface traction (pressure) over entire element
                    // Note: positive for outward normal
  double rho;
  static double shp[3][NEN]; // shape functions and derivatives (overwritten)
  static double pts[nip][2];    // quadrature points
  static double wts[nip];       // quadrature weights

  // private member functions
  void setPressureLoadAtNodes();
  double shapeFunction(double xi, double eta);

  Matrix *Ki;
};

#endif
