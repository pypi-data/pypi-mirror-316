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
// Written: fmk 
// Created: May 1998
// Revision: A
//
#include <PenaltyConstraintHandler.h>

#include <AnalysisModel.h>
#include <Domain.h>
#include <FE_Element.h>
#include <DOF_Group.h>
#include <Node.h>
#include <Element.h>
#include <NodeIter.h>
#include <ElementIter.h>
#include <SP_ConstraintIter.h>
#include <SP_Constraint.h>
#include <MP_ConstraintIter.h>
#include <MP_Constraint.h>
#include <Integrator.h>
#include <ID.h>
#include <Subdomain.h>
#include <Channel.h>
#include <FEM_ObjectBroker.h>
#include <PenaltySP_FE.h>
#include <PenaltyMP_FE.h>
#include <elementAPI.h>

void *
OPS_ADD_RUNTIME_VPV(OPS_PenaltyConstraintHandler)
{
    if(OPS_GetNumRemainingInputArgs() < 2) {
	opserr<<"insufficient number of args\n";
	return 0;
    }

    double data[2];
    int numData = 2;
    if (OPS_GetDoubleInput(&numData, &data[0]) < 0) 
      return nullptr;

    return new PenaltyConstraintHandler(data[0], data[1]);
}


PenaltyConstraintHandler::PenaltyConstraintHandler(double sp, double mp)
:ConstraintHandler(HANDLER_TAG_PenaltyConstraintHandler),
 alphaSP(sp), alphaMP(mp)
{

}


PenaltyConstraintHandler::~PenaltyConstraintHandler()
{

}


int
PenaltyConstraintHandler::handle(const ID *nodesLast)
{
    // first check links exist to a Domain and an AnalysisModel object
    Domain *theDomain = this->getDomainPtr();
    AnalysisModel *theModel = this->getAnalysisModelPtr();
    Integrator *theIntegrator = this->getIntegratorPtr();    
    
    if ((theDomain == 0) || (theModel == 0) || (theIntegrator == 0)) {
	opserr << "WARNING PenaltyConstraintHandler::handle() - ";
	opserr << " setLinks() has not been called\n";
	return -1;
    }

    
    // get number of elements and nodes in the domain 
    // and init the theFEs and theDOFs arrays
    int numSPs = 0;
    SP_ConstraintIter &theSPs = theDomain->getDomainAndLoadPatternSPs();
    SP_Constraint *spPtr;
    while ((spPtr = theSPs()) != nullptr)
      numSPs++;
    
    // initialise the DOF_Groups and add them to the AnalysisModel.
    //    : must of course set the initial IDs
    NodeIter &theNod = theDomain->getNodes();
    Node *nodPtr;
    MP_Constraint *mpPtr;    
    DOF_Group *dofPtr;
    
    int numDofGrp = 0;
    int count3 = 0;
    int countDOF =0;
    while ((nodPtr = theNod()) != nullptr) {
	if ((dofPtr = new DOF_Group(numDofGrp++, nodPtr)) == 0) {
	    opserr << "WARNING PenaltyConstraintHandler::handle() ";
	    opserr << "- ran out of memory";
	    opserr << " creating DOF_Group " << numDofGrp << endln;	
	    return -4;    		
	}

	// initially set all the ID value to -2
	const ID &id = dofPtr->getID();
	for (int j=0; j < id.Size(); j++) {
	    dofPtr->setID(j,-2);
	    countDOF++;
	}
	nodPtr->setDOF_GroupPtr(dofPtr);
	theModel->addDOF_Group(dofPtr);
    }

    theModel->setNumEqn(countDOF);

    // set the number of eqn in the model
    // now see if we have to set any of the dof's to -3
    //    int numLast = 0;
    if (nodesLast != 0) 
	for (int i=0; i<nodesLast->Size(); i++) {
	    int nodeID = (*nodesLast)(i);
	    Node *nodPtr = theDomain->getNode(nodeID);
	    if (nodPtr != 0) {
		dofPtr = nodPtr->getDOF_GroupPtr();
		
		const ID &id = dofPtr->getID();
		// set all the dof values to -3
		for (int j=0; j < id.Size(); j++) 
		    if (id(j) == -2) {
			dofPtr->setID(j,-3);
			count3++;
		    } else {
			opserr << "WARNING PenaltyConstraintHandler::handle() ";
			opserr << " - boundary sp constraint in subdomain";
			opserr << " this should not be - results suspect \n";
		    }
	    }
	}

    // create the FE_Elements for the Elements and add to the AnalysisModel
    ElementIter &theEle = theDomain->getElements();
    Element *elePtr;

    int numFeEle = 0;
    FE_Element *fePtr;
    while ((elePtr = theEle()) != nullptr) {

      // only create an FE_Element for a subdomain element if it does not
      // do independent analysis .. then subdomain part of this analysis so create
      // an FE_element & set subdomain to point to it.
      if (elePtr->isSubdomain() == true) {
	Subdomain *theSub = (Subdomain *)elePtr;
	if (theSub->doesIndependentAnalysis() == false) {
          fePtr = new FE_Element(numFeEle++, elePtr);
	  theModel->addFE_Element(fePtr);
	  theSub->setFE_ElementPtr(fePtr);
	}

      } else {	
	// just a regular element .. create an FE_Element for it & add to AnalysisModel
        fePtr = new FE_Element(numFeEle++, elePtr);	
	theModel->addFE_Element(fePtr);
      }
    }
    

    // create the PenaltySP_FE for the SP_Constraints and 
    // add to the AnalysisModel
    SP_ConstraintIter &theSPss = theDomain->getDomainAndLoadPatternSPs();
    while ((spPtr = theSPss()) != nullptr) {
        fePtr = new PenaltySP_FE(numFeEle, *theDomain, *spPtr, alphaSP);
	theModel->addFE_Element(fePtr);
	numFeEle++;
    }	    

    // create the PenaltyMP_FE for the MP_Constraints and 
    // add to the AnalysisModel
    MP_ConstraintIter &theMPs = theDomain->getMPs();
    while ((mpPtr = theMPs()) != nullptr) {
        fePtr = new PenaltyMP_FE(numFeEle, *theDomain, *mpPtr, alphaMP);
	theModel->addFE_Element(fePtr);
	numFeEle++;
    }	        
    
    return count3;
}


void 
PenaltyConstraintHandler::clearAll(void)
{
    // for the nodes reset the DOF_Group pointers to 0
    Domain *theDomain = this->getDomainPtr();
    if (theDomain == nullptr)
	return;

    NodeIter &theNod = theDomain->getNodes();
    Node *nodPtr;
    while ((nodPtr = theNod()) != nullptr)
	nodPtr->setDOF_GroupPtr(nullptr);
}    

int
PenaltyConstraintHandler::sendSelf(int cTag, Channel &theChannel)
{
  Vector data(2);
  int result = 0;
  data(0) = alphaSP;
  data(1) = alphaMP;
  result = theChannel.sendVector(this->getDbTag(), cTag, data);
  if (result != 0) 
    opserr << "PenaltyConstraintHandler::sendSelf() - error sending Vector\n";
  return result;
}

int
PenaltyConstraintHandler::recvSelf(int cTag, 
				   Channel &theChannel, 
				   FEM_ObjectBroker &theBroker)  
{
  Vector data(2);
  int result = 0;
  result = theChannel.recvVector(this->getDbTag(), cTag, data);
  alphaSP = data(0);
  alphaMP = data(1);
  if (result != 0) 
    opserr << "PenaltyConstraintHandler::recvSelf() - error receiving Vector\n";
  return result;
}

