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
// Purpose: This file contains the class implementation of CTestRelativeTotalNormDispIncr.
//
// Written: Andreas Schellenberg (andreas.schellenberg@gmx.net)
// Created: 05/05
// Revision: A
//
#include <CTestRelativeTotalNormDispIncr.h>
#include <Vector.h>
#include <Channel.h>
#include <EquiSolnAlgo.h>
#include <LinearSOE.h>
#include <Logging.h>

CTestRelativeTotalNormDispIncr::CTestRelativeTotalNormDispIncr()
    : ConvergenceTest(CONVERGENCE_TEST_CTestRelativeTotalNormDispIncr),
    theSOE(0), tol(0), maxNumIter(0), currentIter(0), printFlag(0),
    norms(1), totNorm(0.0), nType(2)
{

}


CTestRelativeTotalNormDispIncr::CTestRelativeTotalNormDispIncr(double theTol, int maxIter, int printIt, int normType)
    : ConvergenceTest(CONVERGENCE_TEST_CTestRelativeTotalNormDispIncr),
    theSOE(0), tol(theTol), maxNumIter(maxIter), currentIter(0), printFlag(printIt),
    norms(maxIter), totNorm(0.0), nType(normType)
{

}


CTestRelativeTotalNormDispIncr::~CTestRelativeTotalNormDispIncr()
{

}


ConvergenceTest* CTestRelativeTotalNormDispIncr::getCopy(int iterations)
{
    CTestRelativeTotalNormDispIncr *theCopy;
    theCopy = new CTestRelativeTotalNormDispIncr(this->tol, iterations, this->printFlag, this->nType);

    theCopy->theSOE = this->theSOE ;

    return theCopy;
}


void CTestRelativeTotalNormDispIncr::setTolerance(double newTol)
{
    tol = newTol;
}


int CTestRelativeTotalNormDispIncr::setEquiSolnAlgo(EquiSolnAlgo &theAlgo)
{
    theSOE = theAlgo.getLinearSOEptr();

    return 0;
}


int CTestRelativeTotalNormDispIncr::test(void)
{
    // check to ensure the SOE has been set - this should not happen if the
    // return from start() is checked
    if (theSOE == 0)  {
        opserr << "WARNING: CTestRelativeTotalNormDispIncr::test() - no SOE set.\n";
        return -1;
    }

    // check to ensure the algo does invoke start() - this is needed otherwise
    // may never get convergence later on in analysis!
    if (currentIter == 0)  {
        opserr << "WARNING: CTestRelativeTotalNormDispIncr::test() - start() was never invoked.\n";
        return -2;
    }

    // get the X vector & determine it's norm & save the value in norms vector
    const Vector &x = theSOE->getX();
    double norm = x.pNorm(nType);
    if (currentIter <= maxNumIter)
        norms(currentIter-1) = norm;

    // add current norm to total norm
    totNorm += norm;

    // get ratio
    if (totNorm != 0.0)
        norm /= totNorm;

    // print the data if required
    if (printFlag & ConvergenceTest::PrintTest)  {
        opserr << LOG_ITERATE 
               << "Iter: "      << pad(currentIter)
               << ", |dR|/|dRtot|: " << pad(norm) 
               << endln;
    }
    if (printFlag & ConvergenceTest::PrintTest02)  {
        opserr << LOG_ITERATE
               << "Iter: "      << pad(currentIter);
        opserr << ", |dR|/|dRtot|: " << pad(norm) 
               << endln;
        opserr << "\tNorm deltaX: "  << pad(norm) 
               << ", Norm deltaR: "  << pad(theSOE->getB().pNorm(nType))
               << endln;
        opserr << "\tdeltaX: "       << x 
               << "\tdeltaR: "       << theSOE->getB();
    }

    //
    // check if the algorithm converged
    //

    // if converged - print & return ok
    if (norm <= tol)  {

        // do some printing first
        if (printFlag & ConvergenceTest::PrintTest || printFlag & ConvergenceTest::PrintTest02)
            opserr << endln;
        else if (printFlag & ConvergenceTest::PrintSuccess)  {
            opserr << LOG_SUCCESS
                   << "Iter: "      << pad(currentIter)
                   << ", |dR|/|dRtot|: " << pad(norm) 
                   << endln;
        }

        // return the number of times test has been called
        return currentIter;
    }

    // algo failed to converged after specified number of iterations - but RETURN OK
    else if ((printFlag & ConvergenceTest::AlwaysSucceed) && currentIter >= maxNumIter)  {
        if (printFlag & ConvergenceTest::PrintFailure) {
            opserr << LOG_FAILURE 
                   //<< "criteria CTestRelativeTotalNormDispIncr but going on"
                   // << LOG_CONTINUE
                   << "Iter: "      << pad(currentIter)
                   << ", |dR|/|dRtot|: " << pad(norm) 
                   << endln
                   << "\tNorm deltaX: "  << pad(norm)
                   << ", Norm deltaR: "  << pad(theSOE->getB().pNorm(nType)) 
                   << endln;
        }
        return currentIter;
    }

    // algo failed to converged after specified number of iterations - return FAILURE -2
    else if (currentIter >= maxNumIter)  { // failes to converge
        if (printFlag & ConvergenceTest::PrintFailure) {
            opserr << LOG_FAILURE
                   //<< "criteria CTestRelativeTotalNormDispIncr"
                   // << LOG_CONTINUE
                   << "Iter: "      << pad(currentIter)
                   << ", |dR|/|dRtot|: " << pad(norm) 
                   << endln;
        }
        currentIter++;
        return ConvergenceTest::Failure;
    }

    // algorithm not yet converged - increment counter and return -1
    else {
        currentIter++;
        return ConvergenceTest::Continue;
    }
}


int CTestRelativeTotalNormDispIncr::start(void)
{
    if (theSOE == 0) {
        opserr << "WARNING: CTestRelativeTotalNormDispIncr::start - no SOE returning true\n";
        return -1;
    }

    // set iteration count = 1
    norms.Zero();
    currentIter = 1;
    totNorm = 0.0;

    return 0;
}


int CTestRelativeTotalNormDispIncr::getNumTests()
{
    return currentIter;
}


int CTestRelativeTotalNormDispIncr::getMaxNumTests(void)
{
    return maxNumIter;
}


double CTestRelativeTotalNormDispIncr::getRatioNumToMax(void)
{
    double div = maxNumIter;

    return currentIter/div;
}


const Vector& CTestRelativeTotalNormDispIncr::getNorms()
{
    return norms;
}


int CTestRelativeTotalNormDispIncr::sendSelf(int cTag, Channel &theChannel)
{
    int res = 0;
    static Vector x(4);
    x(0) = tol;
    x(1) = maxNumIter;
    x(2) = printFlag;
    x(3) = nType;
    res = theChannel.sendVector(this->getDbTag(), cTag, x);
    if (res < 0)
        opserr << "CTestRelativeTotalNormDispIncr::sendSelf() - failed to send data\n";

    return res;
}


int CTestRelativeTotalNormDispIncr::recvSelf(int cTag, Channel &theChannel,
    FEM_ObjectBroker &theBroker)
{
    int res = 0;
    static Vector x(4);
    res = theChannel.recvVector(this->getDbTag(), cTag, x);

    if (res < 0) {
        opserr << "CTestRelativeTotalNormDispIncr::sendSelf() - failed to send data\n";
        tol = 1.0e-8;
        maxNumIter = 25;
        printFlag = 0;
        nType = 2;
    }
    else {
        tol = x(0);
        maxNumIter = (int) x(1);
        printFlag = (int) x(2);
        nType = (int) x(3);
        norms.resize(maxNumIter);
    }

    return res;
}
