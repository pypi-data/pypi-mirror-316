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
// Description: This file contains the implementation for the CrdTransf class.
// CrdTransf provides the abstraction of a frame 
// coordinate transformation. It is an abstract base class and 
// thus no objects of its type can be instatiated. 
//
// Written: Remo Magalhaes de Souza (rmsouza@ce.berkeley.edu)
// Created: 04/2000
// Revision: A
//
#include <CrdTransf.h>
#include <ID.h>
#include <Vector.h>

#include <TaggedObject.h>
#include <MapOfTaggedObjects.h>
#include <api/runtimeAPI.h>
#include <GenericResponse.h>

typedef GenericResponse<CrdTransf> CrdTransfResponse;

static MapOfTaggedObjects theCrdTransfObjects;

void
OPS_ADD_RUNTIME_VXV(OPS_clearAllCrdTransf)
{
  theCrdTransfObjects.clearAll();
}

ID OPS_getAllCrdTransfTags() {

    ID allCrdTransfTags(0);
      
    MapOfTaggedObjectsIter theObjects = theCrdTransfObjects.getIter();
    theObjects.reset();
    TaggedObject *theObject;

    while ((theObject = theObjects()) != 0) {
      CrdTransf *theTransf = (CrdTransf *)theObject;    
      allCrdTransfTags.insert(theTransf->getTag());
    }

    return allCrdTransfTags;
}



// constructor:
CrdTransf::CrdTransf(int tag, int classTag):TaggedObject(tag), MovableObject(classTag)
{
}

// destructor:
CrdTransf::~CrdTransf()
{
}

int
CrdTransf::getLocalAxes(Vector &xAxis, Vector &yAxis, Vector &zAxis)
{
  xAxis.Zero();
  yAxis.Zero();
  zAxis.Zero();
  
  return 0;
}

int
CrdTransf::getRigidOffsets(Vector &offsets)
{
  offsets.Zero();
  
  return 0;
}

Response*
CrdTransf::setResponse(const char **argv, int argc, OPS_Stream &theHandler)
{
  if (argc < 1)
    return 0;

  Response *theResponse = 0;
  
  if (strcmp(argv[0],"xaxis") == 0 || strcmp(argv[0],"xlocal") == 0)
    theResponse = new CrdTransfResponse(*this, 201, Vector(3));
  
  if (strcmp(argv[0],"yaxis") == 0 || strcmp(argv[0],"ylocal") == 0)
    theResponse = new CrdTransfResponse(*this, 202, Vector(3));
  
  if (strcmp(argv[0],"zaxis") == 0 || strcmp(argv[0],"zlocal") == 0)
    theResponse = new CrdTransfResponse(*this, 203, Vector(3));

  if (strcmp(argv[0],"offsets") == 0 || strcmp(argv[0],"rigidOffsets") == 0)
    theResponse = new CrdTransfResponse(*this, 204, Vector(6));
  
  return theResponse;
}

int
CrdTransf::getResponse(int responseID, Information &eleInfo)
{
    if (responseID >= 201 && responseID <= 203) {
        static Vector xlocal(3);
        static Vector ylocal(3);
        static Vector zlocal(3);
        
        this->getLocalAxes(xlocal, ylocal, zlocal);
        
        if (responseID == 201)
            return eleInfo.setVector(xlocal);
        else if (responseID == 202)
            return eleInfo.setVector(ylocal);
        else if (responseID == 203)
            return eleInfo.setVector(zlocal);
        else
            return -1;
    }
    if (responseID == 204) {
      static Vector offsets(6);
      
      offsets.Zero();
      this->getRigidOffsets(offsets);

      return eleInfo.setVector(offsets);
    }
    else
        return -1;
}

const Vector &
CrdTransf::getBasicDisplTotalGrad(int gradNumber)
{
    opserr << "WARNING CrdTransf::getBasicDisplTotalGrad() - this method "
        << " should not be called." << endln;
    
    static Vector dummy(1);
    return dummy;
}

const Vector &
CrdTransf::getGlobalResistingForceShapeSensitivity(const Vector &pb,
						   const Vector &p0,
						   int gradNumber)
{
    opserr << "ERROR CrdTransf::getGlobalResistingForceSensitivity() - has not been"
        << " implemented yet for the chosen transformation." << endln;
    
    static Vector dummy(1);
    return dummy;
}

#if 0
const Vector &
CrdTransf::getGlobalResistingForceShapeSensitivity(const Vector &pb,
						   const Vector &p0)
{
    opserr << "ERROR CrdTransf::getGlobalResistingForceSensitivity() - has not been"
        << " implemented yet for the chosen transformation." << endln;
    
    static Vector dummy(1);
    return dummy;
}
#endif

const Vector &
CrdTransf::getBasicDisplFixedGrad()
{
    opserr << "ERROR CrdTransf::getBasicDisplFixedGrad() - has not been"
           << " implemented yet for the chosen transformation." << endln;
    
    static Vector dummy(1);
    return dummy;
}

