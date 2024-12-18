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
// Written: fmk 11/95
// Revised:
//
// Purpose: This file contains the class definition for ElasticBeam2d.
// ElasticBeam2d is a plane frame member.

#ifndef ElasticBeam2d_h
#define ElasticBeam2d_h

#include <Element.h>
#include <Node.h>
#include <Matrix.h>
#include <Vector.h>
#include <MatrixND.h>
#include <VectorND.h>

class Channel;
class Information;
class CrdTransf;
class SectionForceDeformation;
class Response;

class ElasticBeam2d : public Element
{
  public:
    ElasticBeam2d();        
    ElasticBeam2d(int tag, double A, double E, double I, 
		  int Nd1, int Nd2, CrdTransf &theTransf,
		  double alpha = 0.0, double d = 0.0,
		  double rho = 0.0, int cMass = 0,
		  int release = 0);
    ElasticBeam2d(int tag, int Nd1, int Nd2, 
		  SectionForceDeformation& theSection, CrdTransf &theTransf,
		  double alpha = 0.0, double d = 0.0,
		  double rho = 0.0, int cMass = 0,
		  int release = 0);

    ~ElasticBeam2d();

    const char *getClassType() const {return "ElasticBeam2d";};
    static constexpr const char* class_name = "ElasticBeam2d";

    int getNumExternalNodes() const;
    const ID &getExternalNodes();
    Node **getNodePtrs();

    int getNumDOF();
    void setDomain(Domain *theDomain);
    
    int commitState();
    int revertToLastCommit();        
    int revertToStart();
    
    int update();
    const Matrix &getTangentStiff();
    const Matrix &getInitialStiff();
    const Matrix &getMass();    

    void zeroLoad();	
    int addLoad(ElementalLoad *theLoad, double loadFactor);
    int addInertiaLoadToUnbalance(const Vector &accel);

    const Vector &getResistingForce();
    const Vector &getResistingForceIncInertia();            
    
    int sendSelf(int commitTag, Channel &theChannel);
    int recvSelf(int commitTag, Channel &theChannel, FEM_ObjectBroker &theBroker);
    
    void Print(OPS_Stream &s, int flag = 0);

    Response *setResponse (const char **argv, int argc, OPS_Stream &s);
    int getResponse (int responseID, Information &info);
 
    int setParameter (const char **argv, int argc, Parameter &param);
    int updateParameter (int parameterID, Information &info);

  private:
    double A,E,I;     // area, elastic modulus, moment of inertia
    double alpha,     // coeff. of thermal expansion,
           depth;     // depth
    double rho;       // mass per unit length
    int cMass;        // consistent mass flag

    int release;      // moment release 0=none, 1=I, 2=J, 3=I,J
                      //
    Vector Q;    
    OpenSees::MatrixND<3,3> kb;
    OpenSees::MatrixND<6,6> M;   // mass matrix

    OpenSees::VectorND<3>   q;
    OpenSees::VectorND<3>   q0;  // Fixed end forces in basic system
    OpenSees::VectorND<3>   p0;  // Reactions in basic system
    
    Node *theNodes[2];
    
    ID  connectedExternalNodes;    

    CrdTransf *theCoordTransf;
    
    static Matrix K;
    static Vector P;
};

#endif
