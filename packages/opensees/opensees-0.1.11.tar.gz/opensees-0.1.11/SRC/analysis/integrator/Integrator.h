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
// Description: This file contains the class interface for Integrator.
// Integrator encapsulates the interface provided to FE_Elements and
// DOF_Groups.
//
// For the interface used by the Algorithm and Analysis, 
// see IncrementalIntegrator
//
// Integrator is an abstract base class.
// 
// Written: fmk 
// Created: 11/96
// Revision: A
//
#ifndef Integrator_h
#define Integrator_h

#include <MovableObject.h>
class OPS_Stream;
class FE_Element;
class DOF_Group;
class Vector;
class ID;


class Integrator: public MovableObject
{
public:
    Integrator(int classTag);
    virtual ~Integrator(); 

    virtual int formEleTangent(FE_Element *theEle)  =0;
    virtual int formNodTangent(DOF_Group *theDof)   =0;
    virtual int formEleResidual(FE_Element *theEle) =0;
    virtual int formNodUnbalance(DOF_Group *theDof) =0;    

    virtual int domainChanged() ;

    // Methods provided for Domain Decomposition. This
    // is implemented in IncrementalIntegrator, but is
    // part of the Integrator interface for FE_Elements
    virtual int getLastResponse(Vector &result, const ID &id) =0;

    // Method provided for Output
    virtual void Print(OPS_Stream &s, int flag =0) =0;

    // Sensitivity Integrator interface
    virtual int formSensitivityRHS(int gradNum);
    virtual int formIndependentSensitivityRHS();
    virtual int saveSensitivity   (const Vector &v, int gradNum, int numGrads);
    virtual int commitSensitivity (int gradNum, int numGrads);

    ////////////////////////////////Abbas//////////////////
    virtual int formEleTangentSensitivity(FE_Element *theEle, int gradNumber);  
//  virtual double getLambdaSensitivity(int gradNumber);
    virtual int computeSensitivities();
    int sensitivityDomainChanged();
    bool shouldComputeAtEachStep();
    void setComputeType(int flag);
    bool newAlgorithm() {return true;}
    virtual  bool computeSensitivityAtEachIteration();    
    void activateSensitivityKey() {SensitivityKey=true;}
    bool activateSensitivity() {return SensitivityKey;};


protected:
private:
    int analysisTypeTag;
    bool SensitivityKey;
};

#endif






