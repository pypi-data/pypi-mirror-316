

#include <Parsing.h>

#include <Dynamic/TRBDF3.h>
int
TclCommand_createTRBDF3() {
  return new TRBDF3();
}

#include <Dynamic/Houbolt.h>
int
TclCommand_createHoubolt() {
  return new Houbolt(); 
}

#include <Dynamic/AlphaOSGeneralized.h>
#include <Dynamic/AlphaOSGeneralized_TP.h>
int
TclCommand_createAlphaOSGeneralized(ClientData clientData, Tcl_Interp* interp, int argc, TCL_Char**const argv) {
  // pointer to an integrator that will be returned
  TransientIntegrator *theIntegrator = 0;

  int argc = OPS_GetNumRemainingInputArgs();
  if (argc != 1 && argc != 2 && argc != 4 && argc != 5) {
    opserr << "WARNING - incorrect number of args want AlphaOSGeneralized "
              "$rhoInf <-updateElemDisp>\n";
    opserr << "          or AlphaOSGeneralized $alphaI $alphaF $beta $gamma "
              "<-updateElemDisp>\n";
    return TCL_ERROR;
  }

  bool updElemDisp = false;
  double dData[4];
  int numData;
  if (argc < 3)
    numData = 1;
  else
    numData = 4;

  if (OPS_GetDouble(&numData, dData) != 0) {
    opserr << "WARNING - invalid args want AlphaOSGeneralized $alpha "
              "<-updateElemDisp>\n";
    opserr << "          or AlphaOSGeneralized $alphaI $alphaF $beta $gamma "
              "<-updateElemDisp>\n";
    return TCL_ERROR;
  }

  if (argc == 2 || argc == 5) {
    const char *argvLoc = OPS_GetString();
    if (strcmp(argvLoc, "-updateElemDisp") == 0)
      updElemDisp = true;
  }

  if (argc < 3)
    theIntegrator = new AlphaOSGeneralized(dData[0], updElemDisp);
  else
    theIntegrator = new AlphaOSGeneralized(dData[0], dData[1], dData[2],
                                           dData[3], updElemDisp);

  return theIntegrator;
}


int
TclCommand_createAlphaOSGeneralized_TP(ClientData clientData, Tcl_Interp* interp, int argc, TCL_Char**const argv) {
  // pointer to an integrator that will be returned
  TransientIntegrator *theIntegrator = 0;

  int argc = OPS_GetNumRemainingInputArgs();
  if (argc != 1 && argc != 2 && argc != 4 && argc != 5) {
    opserr << "WARNING - incorrect number of args want AlphaOSGeneralized_TP "
              "$rhoInf <-updateElemDisp>\n";
    opserr << "          or AlphaOSGeneralized_TP $alphaI $alphaF $beta $gamma "
              "<-updateElemDisp>\n";
    return TCL_ERROR;
  }

  bool updElemDisp = false;
  double dData[4];
  int numData;
  if (argc < 3)
    numData = 1;
  else
    numData = 4;

  if (OPS_GetDouble(&numData, dData) != 0) {
    opserr << "WARNING - invalid args want AlphaOSGeneralized_TP $alpha "
              "<-updateElemDisp>\n";
    opserr << "          or AlphaOSGeneralized_TP $alphaI $alphaF $beta $gamma "
              "<-updateElemDisp>\n";
    return TCL_ERROR;
  }

  if (argc == 2 || argc == 5) {
    const char *argvLoc = OPS_GetString();
    if (strcmp(argvLoc, "-updateElemDisp") == 0)
      updElemDisp = true;
  }

  if (argc < 3)
    theIntegrator = new AlphaOSGeneralized_TP(dData[0], updElemDisp);
  else
    theIntegrator = new AlphaOSGeneralized_TP(dData[0], dData[1], dData[2],
                                              dData[3], updElemDisp);

  return theIntegrator;
}




#include <Dynamic/AlphaOS.h>
int
TclCommand_createAlphaOS(ClientData clientData, Tcl_Interp* interp, int argc, TCL_Char**const argv) {
  // pointer to an integrator that will be returned
  TransientIntegrator *theIntegrator = 0;

  int argc = OPS_GetNumRemainingInputArgs();
  if (argc < 1 || argc > 4) {
    opserr << "WARNING - incorrect number of args want AlphaOS $alpha "
              "<-updateElemDisp>\n";
    opserr << "          or AlphaOS $alpha $beta $gamma <-updateElemDisp>\n";
    return TCL_ERROR;
  }

  bool updElemDisp = false;
  double dData[3];
  int numData;
  if (argc < 3)
    numData = 1;
  else
    numData = 3;

  if (OPS_GetDouble(&numData, dData) != 0) {
    opserr << "WARNING - invalid args want AlphaOS $alpha <-updateElemDisp>\n";
    opserr << "          or AlphaOS $alpha $beta $gamma <-updateElemDisp>\n";
    return TCL_ERROR;
  }

  if (argc == 2 || argc == 4) {
    const char *argvLoc = OPS_GetString();
    if (strcmp(argvLoc, "-updateElemDisp") == 0)
      updElemDisp = true;
  }

  if (argc < 3)
    theIntegrator = new AlphaOS(dData[0], updElemDisp);
  else
    theIntegrator = new AlphaOS(dData[0], dData[1], dData[2], updElemDisp);


  return theIntegrator;
}




#include <SRC/analysis/integrator/AlphaOS_TP.h>
int
TclCommand_createAlphaOS_TP(ClientData clientData, Tcl_Interp* interp, int argc, TCL_Char**const argv) {
  // pointer to an integrator that will be returned
  TransientIntegrator *theIntegrator = 0;

  int argc = OPS_GetNumRemainingInputArgs();
  if (argc < 1 || argc > 4) {
    opserr << "WARNING - incorrect number of args want AlphaOS_TP $alpha "
              "<-updateElemDisp>\n";
    opserr << "          or AlphaOS_TP $alpha $beta $gamma <-updateElemDisp>\n";
    return TCL_ERROR;
  }

  bool updElemDisp = false;
  double dData[3];
  int numData;
  if (argc < 3)
    numData = 1;
  else
    numData = 3;

  if (OPS_GetDouble(&numData, dData) != 0) {
    opserr
        << "WARNING - invalid args want AlphaOS_TP $alpha <-updateElemDisp>\n";
    opserr << "          or AlphaOS_TP $alpha $beta $gamma <-updateElemDisp>\n";
    return TCL_ERROR;
  }

  if (argc == 2 || argc == 4) {
    const char *argvLoc = OPS_GetString();
    if (strcmp(argvLoc, "-updateElemDisp") == 0)
      updElemDisp = true;
  }

  if (argc < 3)
    theIntegrator = new AlphaOS_TP(dData[0], updElemDisp);
  else
    theIntegrator = new AlphaOS_TP(dData[0], dData[1], dData[2], updElemDisp);


  return theIntegrator;
}




#include <SRC/analysis/integrator/ArcLength1.h>
int
TclCommand_createArcLength1() {
  double arcLength;
  double alpha;
  if (OPS_GetNumRemainingInputArgs() < 2) {
    opserr << "WARNING integrator ArcLength arcLength alpha \n";
    return TCL_ERROR;
  }

  int numdata = 1;
  if (OPS_GetDoubleInput(&numdata, &arcLength) < 0) {
    opserr << "WARNING integrator ArcLength failed to read arc length\n";
    return TCL_ERROR;
  }
  if (OPS_GetDoubleInput(&numdata, &alpha) < 0) {
    opserr << "WARNING integrator ArcLength failed to read alpha\n";
    return TCL_ERROR;
  }
  return new ArcLength1(arcLength, alpha);
}


#include <SRC/analysis/integrator/ArcLength.h>
int
TclCommand_createArcLength() 
{
  double arcLength;
  double alpha;
  if (OPS_GetNumRemainingInputArgs() < 2) {
    opserr << "WARNING integrator ArcLength arcLength alpha \n";
    return TCL_ERROR;
  }

  int numdata = 1;
  if (OPS_GetDoubleInput(&numdata, &arcLength) < 0) {
    opserr << "WARNING integrator ArcLength failed to read arc lenght\n";
    return TCL_ERROR;
  }
  if (OPS_GetDoubleInput(&numdata, &alpha) < 0) {
    opserr << "WARNING integrator ArcLength failed to read alpha\n";
    return TCL_ERROR;
  }
  return new ArcLength(arcLength, alpha);
}




#include <SRC/analysis/integrator/BackwardEuler.h>
int
TclCommand_createBackwardEuler() {
  int optn = 0;
  if (OPS_GetNumRemainingInputArgs() > 0) {
    int numdata = 1;
    if (OPS_GetIntInput(&numdata, &optn) < 0) {
      opserr << "WARNING integrator BackwardEuler <option> - undefined option "
                "specified\n";
      return TCL_ERROR;
    }
  }
  return new BackwardEuler(optn);
}




#include <SRC/analysis/integrator/CentralDifferenceAlternative.h>
int
TclCommand_createCentralDifferenceAlternative(ClientData clientData, Tcl_Interp* interp, int argc, TCL_Char**const argv) {
  // pointer to an integrator that will be returned
  TransientIntegrator *theIntegrator = 0;

  theIntegrator = new CentralDifferenceAlternative();

  return theIntegrator;
}




#include <SRC/analysis/integrator/CentralDifferenceNoDamping.h>
int
TclCommand_createCentralDifferenceNoDamping(ClientData clientData, Tcl_Interp* interp, int argc, TCL_Char**const argv) {
  // pointer to an integrator that will be returned
  TransientIntegrator *theIntegrator = 0;

  theIntegrator = new CentralDifferenceNoDamping();

  return theIntegrator;
}




#include <SRC/analysis/integrator/CentralDifference.h>
int
TclCommand_createCentralDifference(ClientData clientData, Tcl_Interp* interp, int argc, TCL_Char**const argv) {
  // pointer to an integrator that will be returned
  TransientIntegrator *theIntegrator = 0;

  theIntegrator = new CentralDifference();

  return theIntegrator;
}




#include <SRC/analysis/integrator/CollocationHSFixedNumIter.h>
int
TclCommand_createCollocationHSFixedNumIter(ClientData clientData, Tcl_Interp* interp, int argc, TCL_Char**const argv) {
  // pointer to an integrator that will be returned
  TransientIntegrator *theIntegrator = 0;

  int argc = OPS_GetNumRemainingInputArgs();
  if (argc != 1 && argc != 3 && argc != 5) {
    opserr << "WARNING - incorrect number of args want "
              "CollocationHSFixedNumIter $theta <-polyOrder $O>\n";
    opserr << "          or CollocationHSFixedNumIter $theta $beta $gamma "
              "<-polyOrder $O>\n";
    return TCL_ERROR;
  }

  double dData[3];
  int polyOrder = 2;
  int numData = 0;

  // count number of numeric parameters
  while (OPS_GetNumRemainingInputArgs() > 0) {
    const char *argvLoc = OPS_GetString();
    if (strcmp(argvLoc, "-polyOrder") == 0) {
      break;
    }
    numData++;
  }
  // reset to read from beginning
  OPS_ResetCurrentInputArg(2);

  if (OPS_GetDouble(&numData, dData) != 0) {
    opserr << "WARNING - invalid args want CollocationHSFixedNumIter $theta "
              "<-polyOrder $O>\n";
    opserr << "          or CollocationHSFixedNumIter $theta $beta $gamma "
              "<-polyOrder $O>\n";
    return TCL_ERROR;
  }

  if (numData + 2 == argc) {
    const char *argvLoc = OPS_GetString();
    if (strcmp(argvLoc, "-polyOrder") == 0) {
      int numData2 = 1;
      if (OPS_GetInt(&numData2, &polyOrder) != 0) {
        opserr << "WARNING - invalid polyOrder want CollocationHSFixedNumIter "
                  "$rhoInf <-polyOrder $O>\n";
        opserr << "          or CollocationHSFixedNumIter $alphaI $alphaF "
                  "$beta $gamma <-polyOrder $O>\n";
      }
    }
  }

  if (numData == 1)
    theIntegrator = new CollocationHSFixedNumIter(dData[0], polyOrder);
  else if (numData == 3)
    theIntegrator =
        new CollocationHSFixedNumIter(dData[0], dData[1], dData[2], polyOrder);

  return theIntegrator;
}




#include <SRC/analysis/integrator/CollocationHSIncrLimit.h>
int
TclCommand_createCollocationHSIncrLimit(ClientData clientData, Tcl_Interp* interp, int argc, TCL_Char**const argv) {
  // pointer to an integrator that will be returned
  TransientIntegrator *theIntegrator = 0;

  int argc = OPS_GetNumRemainingInputArgs();
  if (argc != 2 && argc != 4 && argc != 6) {
    opserr << "WARNING - incorrect number of args want CollocationHSIncrLimit "
              "$theta $limit <-normType $T>\n";
    opserr << "          or CollocationHSIncrLimit $theta $beta $gamma $limit "
              "<-normType $T>\n";
    return TCL_ERROR;
  }

  double dData[4];
  int normType = 2;
  int numData = 0;

  // count number of numeric parameters
  while (OPS_GetNumRemainingInputArgs() > 0) {
    const char *argvLoc = OPS_GetString();
    if (strcmp(argvLoc, "-normType") == 0) {
      break;
    }
    numData++;
  }
  // reset to read from beginning
  OPS_ResetCurrentInputArg(2);

  if (OPS_GetDouble(&numData, dData) != 0) {
    opserr << "WARNING - invalid args want CollocationHSIncrLimit $theta "
              "$limit <-normType $T>\n";
    opserr << "          or CollocationHSIncrLimit $theta $beta $gamma $limit "
              "<-normType $T>\n";
    return TCL_ERROR;
  }

  if (numData + 2 == argc) {
    const char *argvLoc = OPS_GetString();
    if (strcmp(argvLoc, "-normType") == 0) {
      int numData2 = 1;
      if (OPS_GetInt(&numData2, &normType) != 0) {
        opserr << "WARNING - invalid normType want CollocationHSIncrLimit "
                  "$theta $limit <-normType $T>\n";
        opserr << "          or CollocationHSIncrLimit $theta $beta $gamma "
                  "$limit <-normType $T>\n";
      }
    }
  }

  if (numData == 2)
    theIntegrator = new CollocationHSIncrLimit(dData[0], dData[1], normType);
  else if (numData == 4)
    theIntegrator = new CollocationHSIncrLimit(dData[0], dData[1], dData[2],
                                               dData[3], normType);


  return theIntegrator;
}




#include <SRC/analysis/integrator/CollocationHSIncrReduct.h>
int
TclCommand_createCollocationHSIncrReduct(ClientData clientData, Tcl_Interp* interp, int argc, TCL_Char**const argv) {
  // pointer to an integrator that will be returned
  TransientIntegrator *theIntegrator = 0;

  int argc = OPS_GetNumRemainingInputArgs();
  if (argc != 2 && argc != 4) {
    opserr << "WARNING - incorrect number of args want CollocationHSIncrReduct "
              "$theta $reduct\n";
    opserr
        << "          or CollocationHSIncrReduct $theta $beta $gamma $reduct\n";
    return TCL_ERROR;
  }

  double dData[4];
  if (OPS_GetDouble(&argc, dData) != 0) {
    opserr << "WARNING - invalid args want CollocationHSIncrReduct $theta "
              "$reduct\n";
    opserr
        << "          or CollocationHSIncrReduct $theta $beta $gamma $reduct\n";
    return TCL_ERROR;
  }

  if (argc == 2)
    theIntegrator = new CollocationHSIncrReduct(dData[0], dData[1]);
  else
    theIntegrator =
        new CollocationHSIncrReduct(dData[0], dData[1], dData[2], dData[3]);

  if (theIntegrator == 0)
    opserr << "WARNING - out of memory creating CollocationHSIncrReduct "
              "integrator\n";

  return theIntegrator;
}




#include <SRC/analysis/integrator/Collocation.h>
int
TclCommand_createCollocation(ClientData clientData, Tcl_Interp* interp, int argc, TCL_Char**const argv) {
  // pointer to an integrator that will be returned
  TransientIntegrator *theIntegrator = 0;

  int argc = OPS_GetNumRemainingInputArgs();
  if (argc != 1 && argc != 3) {
    opserr << "WARNING - incorrect number of args want Collocation $theta\n";
    opserr << "          or Collocation $theta $beta $gamma\n";
    return TCL_ERROR;
  }

  double dData[3];
  if (OPS_GetDouble(&argc, dData) != 0) {
    opserr << "WARNING - invalid args want Collocation $theta\n";
    opserr << "          or Collocation $theta $beta $gamma\n";
    return TCL_ERROR;
  }

  if (argc == 1)
    theIntegrator = new Collocation(dData[0]);
  else
    theIntegrator = new Collocation(dData[0], dData[1], dData[2]);

  return theIntegrator;
}




#include <SRC/analysis/integrator/DisplacementControl.h>
int
TclCommand_createDisplacementControlIntegrator() {
  if (OPS_GetNumRemainingInputArgs() < 3) {
    opserr << "insufficient arguments for DisplacementControl\n";
    return TCL_ERROR;
  }

  // node, dof
  int iData[2];
  int numData = 2;
  if (OPS_GetIntInput(&numData, &iData[0]) < 0) {
    opserr << "WARNING failed to read node tag and ndf\n";
    return TCL_ERROR;
  }

  double incr;
  numData = 1;
  if (OPS_GetDoubleInput(&numData, &incr) < 0) {
    opserr << "WARNING failed to read incr\n";
    return TCL_ERROR;
  }

  // numIter,dumin,dumax
  int numIter = 1;
  int formTangent = 0;
  double data[2] = {incr, incr};
  if (OPS_GetNumRemainingInputArgs() > 2) {
    numData = 1;
    if (OPS_GetIntInput(&numData, &numIter) < 0) {
      opserr << "WARNING failed to read numIter\n";
      return TCL_ERROR;
    }
    numData = 2;
    if (OPS_GetDoubleInput(&numData, &data[0]) < 0) {
      opserr << "WARNING failed to read dumin and dumax\n";
      return TCL_ERROR;
    }
  }

  if (OPS_GetNumRemainingInputArgs() == 1) {
    std::string type = OPS_GetString();
    if (type == "-initial" || type == "-Initial") {
      formTangent = 1;
    }
  }

  // check node
  Domain *theDomain = OPS_GetDomain();
  Node *theNode = theDomain->getNode(iData[0]);
  if (theNode == 0) {
    opserr << "WARNING integrator DisplacementControl node dof dU : Node does "
              "not exist\n";
    return TCL_ERROR;
  }

  int numDOF = theNode->getNumberDOF();
  if (iData[1] <= 0 || iData[1] > numDOF) {
    opserr << "WARNING integrator DisplacementControl node dof dU : invalid "
              "dof given\n";
    return TCL_ERROR;
  }

  return new DisplacementControl(iData[0], iData[1] - 1, incr, theDomain,
                                 numIter, data[0], data[1], formTangent);
}



#include <SRC/analysis/integrator/ExplicitDifference.h>
int
TclCommand_createExplicitDifference(ClientData clientData, Tcl_Interp* interp, int argc, TCL_Char**const argv) {
  TransientIntegrator *theIntegrator = 0;
  theIntegrator = new ExplicitDifference();

  return theIntegrator;
}




#include <SRC/analysis/integrator/GeneralizedAlpha.h>
int
TclCommand_createGeneralizedAlpha(ClientData clientData, Tcl_Interp* interp, int argc, TCL_Char**const argv) {
  // Pointer to an integrator that will be returned
  TransientIntegrator *theIntegrator = 0;

  int argc = OPS_GetNumRemainingInputArgs();
  if (argc != 2 && argc != 4) {
    opserr << "WARNING - incorrect number of args want GeneralizedAlpha "
              "$alphaM $alphaF <$gamma $beta>\n";
    return TCL_ERROR;
  }

  double dData[4];
  if (OPS_GetDouble(&argc, dData) != 0) {
    opserr << "WARNING - invalid args want GeneralizedAlpha $alphaM $alphaF "
              "<$gamma $beta>\n";
    return TCL_ERROR;
  }

  if (argc == 2)
    theIntegrator = new GeneralizedAlpha(dData[0], dData[1]);
  else
    theIntegrator =
        new GeneralizedAlpha(dData[0], dData[1], dData[2], dData[3]);

  return theIntegrator;
}




#include <SRC/analysis/integrator/GimmeMCK.h>
int
TclCommand_createGimmeMCK(ClientData clientData, Tcl_Interp* interp, int argc, TCL_Char**const argv) {
  // pointer to an integrator that will be returned
  TransientIntegrator *theIntegrator = 0;

  int argc = OPS_GetNumRemainingInputArgs();
  if (argc < 3) {
    opserr
        << "WARNING - incorrect number of args want GimmeMCK $m $c $k <$ki>\n";
    return TCL_ERROR;
  }

  int numdata = 3;
  double ddata[3];
  if (OPS_GetDouble(&numdata, ddata) != 0) {
    opserr << "WARNING - invalid args want GimmeMCK $m $c $k <$ki>\n";
    return TCL_ERROR;
  }
  numdata = 1;
  double ki = 0.0;
  if (argc > 3) {
    if (OPS_GetDouble(&numdata, &ki) != 0) {
      opserr << "WARNING - invalid args want GimmeMCK $m $c $k <$ki>\n";
      return TCL_ERROR;
    }
  }

  theIntegrator = new GimmeMCK(ddata[0], ddata[1], ddata[2], ki);


  return theIntegrator;
}




#include <SRC/analysis/integrator/HarmonicSteadyState.h>
int
TclCommand_createHarmonicSteadyState() {
  if (OPS_GetNumRemainingInputArgs() < 2) {
    opserr << "insufficient arguments\n";
    return TCL_ERROR;
  }

  double lambda;
  int numData = 1;
  if (OPS_GetDoubleInput(&numData, &lambda) < 0) {
    opserr << "WARNING failed to read double lambda\n";
    return TCL_ERROR;
  }

  double period = 0;
  numData = 1;
  if (OPS_GetDoubleInput(&numData, &period) < 0) {
    opserr << "WARNING failed to read double period\n";
    return TCL_ERROR;
  }

  int numIter = 1;
  double mLambda[2] = {lambda, lambda};
  if (OPS_GetNumRemainingInputArgs() > 2) {
    if (OPS_GetIntInput(&numData, &numIter) < 0) {
      opserr << "WARNING failed to read int numIter\n";
      return TCL_ERROR;
    }
    numData = 2;
    if (OPS_GetDoubleInput(&numData, &mLambda[0]) < 0) {
      opserr << "WARNING failed to read double min and max\n";
      return TCL_ERROR;
    }
  }

  return new HarmonicSteadyState(lambda, period, numIter, mLambda[0],
                                 mLambda[1]);
}




#include <SRC/analysis/integrator/HHTExplicit.h>
int
TclCommand_createHHTExplicit(ClientData clientData, Tcl_Interp* interp, int argc, TCL_Char**const argv) {
  // pointer to an integrator that will be returned
  TransientIntegrator *theIntegrator = 0;

  int argc = OPS_GetNumRemainingInputArgs();
  if (argc < 1 || argc > 3) {
    opserr << "WARNING - incorrect number of args want HHTExplicit $alpha "
              "<-updateElemDisp>\n";
    opserr << "          or HHTExplicit $alpha $gamma <-updateElemDisp>\n";
    return TCL_ERROR;
  }

  bool updElemDisp = false;
  double dData[2];
  int numData = 0;

  // count number of numeric parameters
  while (OPS_GetNumRemainingInputArgs() > 0) {
    const char *argvLoc = OPS_GetString();
    if (strcmp(argvLoc, "-updateElemDisp") == 0) {
      break;
    }
    numData++;
  }
  // reset to read from beginning
  OPS_ResetCurrentInputArg(2);

  if (OPS_GetDouble(&numData, dData) != 0) {
    opserr
        << "WARNING - invalid args want HHTExplicit $alpha <-updateElemDisp>\n";
    opserr << "          or HHTExplicit $alpha $gamma <-updateElemDisp>\n";
    return TCL_ERROR;
  }

  if (numData + 1 == argc) {
    const char *argvLoc = OPS_GetString();
    if (strcmp(argvLoc, "-updateElemDisp") == 0)
      updElemDisp = true;
  }

  if (numData == 1)
    theIntegrator = new HHTExplicit(dData[0], updElemDisp);
  else if (numData == 2)
    theIntegrator = new HHTExplicit(dData[0], dData[1], updElemDisp);

  return theIntegrator;
}




#include <SRC/analysis/integrator/HHTExplicit_TP.h>
int
TclCommand_createHHTExplicit_TP(ClientData clientData, Tcl_Interp* interp, int argc, TCL_Char**const argv) {
  // pointer to an integrator that will be returned
  TransientIntegrator *theIntegrator = 0;

  int argc = OPS_GetNumRemainingInputArgs();
  if (argc < 1 || argc > 2) {
    opserr << "WARNING - incorrect number of args want HHTExplicit_TP $alpha\n";
    opserr << "          or HHTExplicit_TP $alpha $gamma\n";
    return TCL_ERROR;
  }

  double dData[2];
  if (OPS_GetDouble(&argc, dData) != 0) {
    opserr << "WARNING - invalid args want HHTExplicit_TP $alpha\n";
    opserr << "          or HHTExplicit_TP $alpha $gamma\n";
    return TCL_ERROR;
  }

  if (argc == 1)
    theIntegrator = new HHTExplicit_TP(dData[0]);
  else if (argc == 2)
    theIntegrator = new HHTExplicit_TP(dData[0], dData[1]);

  return theIntegrator;
}




#include <SRC/analysis/integrator/HHTGeneralizedExplicit.h>
int
TclCommand_createHHTGeneralizedExplicit(ClientData clientData, Tcl_Interp* interp, int argc, TCL_Char**const argv) {
  // pointer to an integrator that will be returned
  TransientIntegrator *theIntegrator = 0;

  int argc = OPS_GetNumRemainingInputArgs();
  if (argc < 2 || argc > 5) {
    opserr << "WARNING - incorrect number of args want HHTGeneralizedExplicit "
              "$rhoB $alphaF <-updateElemDisp>\n";
    opserr << "          or HHTGeneralizedExplicit $alphaI $alphaF $beta "
              "$gamma <-updateElemDisp>\n";
    return TCL_ERROR;
  }

  bool updElemDisp = false;
  double dData[4];
  int numData;
  if (argc < 4)
    numData = 2;
  else
    numData = 4;

  if (OPS_GetDouble(&numData, dData) != 0) {
    opserr << "WARNING - invalid args want HHTGeneralizedExplicit $rhoB "
              "$alphaF <-updateElemDisp>\n";
    opserr << "          or HHTGeneralizedExplicit $alphaI $alphaF $beta "
              "$gamma <-updateElemDisp>\n";
    return TCL_ERROR;
  }

  if (argc == 3 || argc == 5) {
    const char *argvLoc = OPS_GetString();
    if (strcmp(argvLoc, "-updateElemDisp") == 0)
      updElemDisp = true;
  }

  if (argc < 4)
    theIntegrator = new HHTGeneralizedExplicit(dData[0], dData[1], updElemDisp);
  else
    theIntegrator = new HHTGeneralizedExplicit(dData[0], dData[1], dData[2],
                                               dData[3], updElemDisp);

  return theIntegrator;
}




#include <SRC/analysis/integrator/HHTGeneralizedExplicit_TP.h>
int
TclCommand_createHHTGeneralizedExplicit_TP(ClientData clientData, Tcl_Interp* interp, int argc, TCL_Char**const argv) {
  // pointer to an integrator that will be returned
  TransientIntegrator *theIntegrator = 0;

  int argc = OPS_GetNumRemainingInputArgs();
  if (argc != 2 && argc != 4) {
    opserr << "WARNING - incorrect number of args want "
              "HHTGeneralizedExplicit_TP $rhoB $alphaF\n";
    opserr << "          or HHTGeneralizedExplicit_TP $alphaI $alphaF $beta "
              "$gamma\n";
    return TCL_ERROR;
  }

  double dData[4];
  if (OPS_GetDouble(&argc, dData) != 0) {
    opserr << "WARNING - invalid args want HHTGeneralizedExplicit_TP $rhoB "
              "$alphaF\n";
    opserr << "          or HHTGeneralizedExplicit_TP $alphaI $alphaF $beta "
              "$gamma\n";
    return TCL_ERROR;
  }

  if (argc == 2)
    theIntegrator = new HHTGeneralizedExplicit_TP(dData[0], dData[1]);
  else if (argc == 4)
    theIntegrator =
        new HHTGeneralizedExplicit_TP(dData[0], dData[1], dData[2], dData[3]);

  return theIntegrator;
}




#include <SRC/analysis/integrator/HHTGeneralized.h>
int
TclCommand_createHHTGeneralized(ClientData clientData, Tcl_Interp* interp, int argc, TCL_Char**const argv) {
  // pointer to an integrator that will be returned
  TransientIntegrator *theIntegrator = 0;

  int argc = OPS_GetNumRemainingInputArgs();
  if (argc != 1 && argc != 4) {
    opserr
        << "WARNING - incorrect number of args want HHTGeneralized $rhoInf\n";
    opserr << "          or HHTGeneralized $alphaI $alphaF $beta $gamma\n";
    return TCL_ERROR;
  }

  double dData[4];
  if (OPS_GetDouble(&argc, dData) != 0) {
    opserr << "WARNING - invalid args want HHTGeneralized $rhoInf\n";
    opserr << "          or HHTGeneralized $alphaI $alphaF $beta $gamma\n";
    return TCL_ERROR;
  }

  if (argc == 1)
    theIntegrator = new HHTGeneralized(dData[0]);
  else
    theIntegrator = new HHTGeneralized(dData[0], dData[1], dData[2], dData[3]);

  return theIntegrator;
}




#include <SRC/analysis/integrator/HHTGeneralized_TP.h>
int
TclCommand_createHHTGeneralized_TP(ClientData clientData, Tcl_Interp* interp, int argc, TCL_Char**const argv) {
  // pointer to an integrator that will be returned
  TransientIntegrator *theIntegrator = 0;

  int argc = OPS_GetNumRemainingInputArgs();
  if (argc != 1 && argc != 4) {
    opserr << "WARNING - incorrect number of args want HHTGeneralized_TP "
              "$rhoInf\n";
    opserr << "          or HHTGeneralized_TP $alphaI $alphaF $beta $gamma\n";
    return TCL_ERROR;
  }

  double dData[4];
  if (OPS_GetDouble(&argc, dData) != 0) {
    opserr << "WARNING - invalid args want HHTGeneralized_TP $rhoInf\n";
    opserr << "          or HHTGeneralized_TP $alphaI $alphaF $beta $gamma\n";
    return TCL_ERROR;
  }

  if (argc == 1)
    theIntegrator = new HHTGeneralized_TP(dData[0]);
  else
    theIntegrator =
        new HHTGeneralized_TP(dData[0], dData[1], dData[2], dData[3]);

  return theIntegrator;
}




#include <SRC/analysis/integrator/HHTHSFixedNumIter.h>
int
TclCommand_createHHTHSFixedNumIter(ClientData clientData, Tcl_Interp* interp, int argc, TCL_Char**const argv) {
  // pointer to an integrator that will be returned
  TransientIntegrator *theIntegrator = 0;

  int argc = OPS_GetNumRemainingInputArgs();
  if (argc != 1 && argc != 3 && argc != 4 && argc != 6) {
    opserr << "WARNING - incorrect number of args want HHTHSFixedNumIter "
              "$rhoInf <-polyOrder $O>\n";
    opserr << "          or HHTHSFixedNumIter $alphaI $alphaF $beta $gamma "
              "<-polyOrder $O>\n";
    return TCL_ERROR;
  }

  double dData[4];
  int polyOrder = 2;
  bool updDomFlag = true;
  int numData;
  if (argc < 4)
    numData = 1;
  else
    numData = 4;

  if (OPS_GetDouble(&numData, dData) != 0) {
    opserr << "WARNING - invalid args want HHTHSFixedNumIter $rhoInf "
              "<-polyOrder $O>\n";
    opserr << "          or HHTHSFixedNumIter $alphaI $alphaF $beta $gamma "
              "<-polyOrder $O>\n";
    return TCL_ERROR;
  }

  if (argc == 3 || argc == 6) {
    const char *argvLoc = OPS_GetString();
    if (strcmp(argvLoc, "-polyOrder") == 0) {
      numData = 1;
      if (OPS_GetInt(&numData, &polyOrder) != 0) {
        opserr << "WARNING - invalid polyOrder want HHTHSFixedNumIter $rhoInf "
                  "<-polyOrder $O>\n";
        opserr << "          or HHTHSFixedNumIter $alphaI $alphaF $beta $gamma "
                  "<-polyOrder $O>\n";
      }
    }
  }

  if (argc < 4)
    theIntegrator = new HHTHSFixedNumIter(dData[0], polyOrder, updDomFlag);
  else
    theIntegrator = new HHTHSFixedNumIter(dData[0], dData[1], dData[2],
                                          dData[3], polyOrder, updDomFlag);

  return theIntegrator;
}




#include <SRC/analysis/integrator/HHTHSFixedNumIter_TP.h>
int
TclCommand_createHHTHSFixedNumIter_TP(ClientData clientData, Tcl_Interp* interp, int argc, TCL_Char**const argv) {
  // pointer to an integrator that will be returned
  TransientIntegrator *theIntegrator = 0;

  int argc = OPS_GetNumRemainingInputArgs();
  if (argc != 1 && argc != 3 && argc != 4 && argc != 6) {
    opserr << "WARNING - incorrect number of args want HHTHSFixedNumIter_TP "
              "$rhoInf <-polyOrder $O>\n";
    opserr << "          or HHTHSFixedNumIter_TP $alphaI $alphaF $beta $gamma "
              "<-polyOrder $O>\n";
    return TCL_ERROR;
  }

  double dData[4];
  int polyOrder = 2;
  bool updDomFlag = true;
  int numData;
  if (argc < 4)
    numData = 1;
  else
    numData = 4;

  if (OPS_GetDouble(&numData, dData) != 0) {
    opserr << "WARNING - invalid args want HHTHSFixedNumIter_TP $rhoInf "
              "<-polyOrder $O>\n";
    opserr << "          or HHTHSFixedNumIter_TP $alphaI $alphaF $beta $gamma "
              "<-polyOrder $O>\n";
    return TCL_ERROR;
  }

  if (argc == 3 || argc == 6) {
    const char *argvLoc = OPS_GetString();
    if (strcmp(argvLoc, "-polyOrder") == 0) {
      numData = 1;
      if (OPS_GetInt(&numData, &polyOrder) != 0) {
        opserr << "WARNING - invalid polyOrder want HHTHSFixedNumIter_TP "
                  "$rhoInf <-polyOrder $O>\n";
        opserr << "          or HHTHSFixedNumIter_TP $alphaI $alphaF $beta "
                  "$gamma <-polyOrder $O>\n";
      }
    }
  }

  if (argc < 4)
    theIntegrator = new HHTHSFixedNumIter_TP(dData[0], polyOrder, updDomFlag);
  else
    theIntegrator = new HHTHSFixedNumIter_TP(dData[0], dData[1], dData[2],
                                             dData[3], polyOrder, updDomFlag);

  return theIntegrator;
}




#include <SRC/analysis/integrator/HHTHSIncrLimit.h>
int
TclCommand_createHHTHSIncrLimit(ClientData clientData, Tcl_Interp* interp, int argc, TCL_Char**const argv) {
  // pointer to an integrator that will be returned
  TransientIntegrator *theIntegrator = 0;

  int argc = OPS_GetNumRemainingInputArgs();
  if (argc != 2 && argc != 4 && argc != 5 && argc != 7) {
    opserr << "WARNING - incorrect number of args want HHTHSIncrLimit $rhoInf "
              "$limit <-normType $T>\n";
    opserr << "          or HHTHSIncrLimit $alphaI $alphaF $beta $gamma $limit "
              "<-normType $T>\n";
    return TCL_ERROR;
  }

  double dData[5];
  int normType = 2;
  int numData;
  if (argc < 5)
    numData = 2;
  else
    numData = 5;

  if (OPS_GetDouble(&numData, dData) != 0) {
    opserr << "WARNING - invalid args want HHTHSIncrLimit $rhoInf $limit "
              "<-normType $T>\n";
    opserr << "          or HHTHSIncrLimit $alphaI $alphaF $beta $gamma $limit "
              "<-normType $T>\n";
    return TCL_ERROR;
  }

  if (argc == 4 || argc == 7) {
    const char *argvLoc = OPS_GetString();
    if (strcmp(argvLoc, "-normType") == 0) {
      numData = 1;
      if (OPS_GetInt(&numData, &normType) != 0) {
        opserr << "WARNING - invalid normType want HHTHSIncrLimit $rhoInf "
                  "$limit <-normType $T>\n";
        opserr << "          or HHTHSIncrLimit $alphaI $alphaF $beta $gamma "
                  "$limit <-normType $T>\n";
      }
    }
  }

  if (argc < 5)
    theIntegrator = new HHTHSIncrLimit(dData[0], dData[1], normType);
  else
    theIntegrator = new HHTHSIncrLimit(dData[0], dData[1], dData[2], dData[3],
                                       dData[4], normType);

  return theIntegrator;
}




#include <SRC/analysis/integrator/HHTHSIncrLimit_TP.h>
int
TclCommand_createHHTHSIncrLimit_TP(ClientData clientData, Tcl_Interp* interp, int argc, TCL_Char**const argv) {
  // pointer to an integrator that will be returned
  TransientIntegrator *theIntegrator = 0;

  int argc = OPS_GetNumRemainingInputArgs();
  if (argc != 2 && argc != 4 && argc != 5 && argc != 7) {
    opserr << "WARNING - incorrect number of args want HHTHSIncrLimit_TP "
              "$rhoInf $limit <-normType $T>\n";
    opserr << "          or HHTHSIncrLimit_TP $alphaI $alphaF $beta $gamma "
              "$limit <-normType $T>\n";
    return TCL_ERROR;
  }

  double dData[5];
  int normType = 2;
  int numData;
  if (argc < 5)
    numData = 2;
  else
    numData = 5;

  if (OPS_GetDouble(&numData, dData) != 0) {
    opserr << "WARNING - invalid args want HHTHSIncrLimit_TP $rhoInf $limit "
              "<-normType $T>\n";
    opserr << "          or HHTHSIncrLimit_TP $alphaI $alphaF $beta $gamma "
              "$limit <-normType $T>\n";
    return TCL_ERROR;
  }

  if (argc == 4 || argc == 7) {
    const char *argvLoc = OPS_GetString();
    if (strcmp(argvLoc, "-normType") == 0) {
      numData = 1;
      if (OPS_GetInt(&numData, &normType) != 0) {
        opserr << "WARNING - invalid normType want HHTHSIncrLimit_TP $rhoInf "
                  "$limit <-normType $T>\n";
        opserr << "          or HHTHSIncrLimit_TP $alphaI $alphaF $beta $gamma "
                  "$limit <-normType $T>\n";
      }
    }
  }

  if (argc < 5)
    theIntegrator = new HHTHSIncrLimit_TP(dData[0], dData[1], normType);
  else
    theIntegrator = new HHTHSIncrLimit_TP(dData[0], dData[1], dData[2],
                                          dData[3], dData[4], normType);

  return theIntegrator;
}




#include <SRC/analysis/integrator/HHTHSIncrReduct.h>
int
TclCommand_createHHTHSIncrReduct(ClientData clientData, Tcl_Interp* interp, int argc, TCL_Char**const argv) {
  // pointer to an integrator that will be returned
  TransientIntegrator *theIntegrator = 0;

  int argc = OPS_GetNumRemainingInputArgs();
  if (argc != 2 && argc != 5) {
    opserr << "WARNING - incorrect number of args want HHTHSIncrReduct $rhoInf "
              "$reduct\n";
    opserr << "          or HHTHSIncrReduct $alphaI $alphaF $beta $gamma "
              "$reduct\n";
    return TCL_ERROR;
  }

  double dData[5];
  if (OPS_GetDouble(&argc, dData) != 0) {
    opserr << "WARNING - invalid args want HHTHSIncrReduct $rhoInf $reduct\n";
    opserr << "          or HHTHSIncrReduct $alphaI $alphaF $beta $gamma "
              "$reduct\n";
    return TCL_ERROR;
  }

  if (argc == 2)
    theIntegrator = new HHTHSIncrReduct(dData[0], dData[1]);
  else
    theIntegrator =
        new HHTHSIncrReduct(dData[0], dData[1], dData[2], dData[3], dData[4]);

  return theIntegrator;
}




#include <SRC/analysis/integrator/HHTHSIncrReduct_TP.h>
int
TclCommand_createHHTHSIncrReduct_TP(ClientData clientData, Tcl_Interp* interp, int argc, TCL_Char**const argv) {
  // pointer to an integrator that will be returned
  TransientIntegrator *theIntegrator = 0;

  int argc = OPS_GetNumRemainingInputArgs();
  if (argc != 2 && argc != 5) {
    opserr << "WARNING - incorrect number of args want HHTHSIncrReduct_TP "
              "$rhoInf $reduct\n";
    opserr << "          or HHTHSIncrReduct_TP $alphaI $alphaF $beta $gamma "
              "$reduct\n";
    return TCL_ERROR;
  }

  double dData[5];
  if (OPS_GetDouble(&argc, dData) != 0) {
    opserr
        << "WARNING - invalid args want HHTHSIncrReduct_TP $rhoInf $reduct\n";
    opserr << "          or HHTHSIncrReduct_TP $alphaI $alphaF $beta $gamma "
              "$reduct\n";
    return TCL_ERROR;
  }

  if (argc == 2)
    theIntegrator = new HHTHSIncrReduct_TP(dData[0], dData[1]);
  else
    theIntegrator = new HHTHSIncrReduct_TP(dData[0], dData[1], dData[2],
                                           dData[3], dData[4]);

  return theIntegrator;
}

#include <SRC/analysis/integrator/HHT.h>

int
TclCommand_createHHT(ClientData clientData, Tcl_Interp* interp, int argc, TCL_Char**const argv) {
  // pointer to an integrator that will be returned
  TransientIntegrator *theIntegrator = 0;

  int argc = OPS_GetNumRemainingInputArgs();
  if (argc != 1 && argc != 3) {
    opserr << "WARNING - incorrect number of args want HHT $alpha <$gamma "
              "$beta>\n";
    return TCL_ERROR;
  }

  double dData[3];
  if (OPS_GetDouble(&argc, dData) != 0) {
    opserr << "WARNING - invalid args want HHT $alpha <$gamma $beta>\n";
    return TCL_ERROR;
  }

  if (argc == 1)
    theIntegrator = new HHT(dData[0]);
  else
    theIntegrator = new HHT(dData[0], dData[1], dData[2]);


  return theIntegrator;
}




#include <SRC/analysis/integrator/HHT_TP.h>
int
TclCommand_createHHT_TP(ClientData clientData, Tcl_Interp* interp, int argc, TCL_Char**const argv) {
  // pointer to an integrator that will be returned
  TransientIntegrator *theIntegrator = 0;

  int argc = OPS_GetNumRemainingInputArgs();
  if (argc != 1 && argc != 3) {
    opserr << "WARNING - incorrect number of args want HHT_TP $alpha <$gamma "
              "$beta>\n";
    return TCL_ERROR;
  }

  double dData[3];
  if (OPS_GetDouble(&argc, dData) != 0) {
    opserr << "WARNING - invalid args want HHT_TP $alpha <$gamma $beta>\n";
    return TCL_ERROR;
  }

  if (argc == 1)
    theIntegrator = new HHT_TP(dData[0]);
  else
    theIntegrator = new HHT_TP(dData[0], dData[1], dData[2]);

  return theIntegrator;
}








#include <SRC/analysis/integrator/HSConstraint.h>
int
TclCommand_createHSConstraint() {
  int numdata = OPS_GetNumRemainingInputArgs();
  if (numdata < 1) {
    opserr << "WARNING integrator HSConstraint <arcLength> <psi_u> <psi_f> "
              "<u_ref> \n";
    return TCL_ERROR;
  }
  if (numdata > 4)
    numdata = 4;

  double data[4];
  if (OPS_GetDoubleInput(&numdata, data) < 0) {
    opserr << "WARNING integrator HSConstraint invalid double inputs\n";
    return TCL_ERROR;
  }
  double arcLength = data[0];
  double psi_u = data[1];
  double psi_f = data[2];
  double u_ref = data[3];

  switch (numdata) {
  case 1:
    return new HSConstraint(arcLength);
  case 2:
    return new HSConstraint(arcLength, psi_u);
  case 3:
    return new HSConstraint(arcLength, psi_u, psi_f);
  case 4:
    return new HSConstraint(arcLength, psi_u, psi_f, u_ref);
  }

  return TCL_ERROR;
}




#include <SRC/analysis/integrator/KRAlphaExplicit.h>
int
TclCommand_createKRAlphaExplicit(ClientData clientData, Tcl_Interp* interp, int argc, TCL_Char**const argv) {
  // pointer to an integrator that will be returned
  TransientIntegrator *theIntegrator = 0;

  int argc = OPS_GetNumRemainingInputArgs();
  if (argc != 1 && argc != 2) {
    opserr << "WARNING - incorrect number of args want KRAlphaExplicit $rhoInf "
              "<-updateElemDisp>\n";
    return TCL_ERROR;
  }

  bool updElemDisp = false;
  double rhoInf;
  int numData = 1;
  if (OPS_GetDouble(&numData, &rhoInf) != 0) {
    opserr << "WARNING - invalid args want KRAlphaExplicit $rhoInf "
              "<-updateElemDisp>\n";
    return TCL_ERROR;
  }

  if (argc == 2) {
    const char *argvLoc = OPS_GetString();
    if (strcmp(argvLoc, "-updateElemDisp") == 0)
      updElemDisp = true;
  }

  theIntegrator = new KRAlphaExplicit(rhoInf, updElemDisp);

  return theIntegrator;
}




#include <SRC/analysis/integrator/KRAlphaExplicit_TP.h>
int
TclCommand_createKRAlphaExplicit_TP(ClientData clientData, Tcl_Interp* interp, int argc, TCL_Char**const argv) {
  // pointer to an integrator that will be returned
  TransientIntegrator *theIntegrator = 0;

  int argc = OPS_GetNumRemainingInputArgs();
  if (argc != 1) {
    opserr << "WARNING - incorrect number of args want KRAlphaExplicit_TP "
              "$rhoInf\n";
    return TCL_ERROR;
  }

  double rhoInf;
  if (OPS_GetDouble(&argc, &rhoInf) != 0) {
    opserr << "WARNING - invalid args want KRAlphaExplicit_TP $rhoInf\n";
    return TCL_ERROR;
  }

  theIntegrator = new KRAlphaExplicit_TP(rhoInf);

  return theIntegrator;
}




#include <SRC/analysis/integrator/LoadControl.h>
int
TclCommand_createLoadControlIntegrator() {
  if (OPS_GetNumRemainingInputArgs() < 1) {
    opserr << "LoadControl - insufficient arguments\n";
    return TCL_ERROR;
  }

  double lambda;
  int numData = 1;
  if (OPS_GetDoubleInput(&numData, &lambda) < 0) {
    opserr << "WARNING LoadControl - failed to read double lambda\n";
    return TCL_ERROR;
  }

  int numIter = 1;
  double mLambda[2] = {lambda, lambda};
  if (OPS_GetNumRemainingInputArgs() > 2) {
    if (OPS_GetIntInput(&numData, &numIter) < 0) {
      opserr << "WARNING LoadControl - failed to read int numIter\n";
      return TCL_ERROR;
    }
    numData = 2;
    if (OPS_GetDoubleInput(&numData, &mLambda[0]) < 0) {
      opserr << "WARNING LoadControl - failed to read double min and max\n";
      return TCL_ERROR;
    }
  }

  return new LoadControl(lambda, numIter, mLambda[0], mLambda[1]);
}




#include <SRC/analysis/integrator/LoadPath.h>




#include <SRC/analysis/integrator/MinUnbalDispNorm.h>
int
TclCommand_createMinUnbalDispNorm() {
  double lambda11, minlambda, maxlambda;
  int numIter;
  if (OPS_GetNumRemainingInputArgs() < 1) {
    opserr << "WARNING integrator MinUnbalDispNorm lambda11 <Jd minLambda1j "
              "maxLambda1j>\n";
    return TCL_ERROR;
  }

  int numdata = 1;
  if (OPS_GetDoubleInput(&numdata, &lambda11) < 0) {
    opserr << "WARNING integrator MinUnbalDispNorm invalid lambda11\n";
    return TCL_ERROR;
  }

  if (OPS_GetNumRemainingInputArgs() >= 3) {
    if (OPS_GetIntInput(&numdata, &numIter) < 0) {
      opserr << "WARNING integrator MinUnbalDispNorm invalid numIter\n";
      return TCL_ERROR;
    }
    if (OPS_GetDoubleInput(&numdata, &minlambda) < 0) {
      opserr << "WARNING integrator MinUnbalDispNorm invalid minlambda\n";
      return TCL_ERROR;
    }
    if (OPS_GetDoubleInput(&numdata, &maxlambda) < 0) {
      opserr << "WARNING integrator MinUnbalDispNorm invalid maxlambda\n";
      return TCL_ERROR;
    }
  } else {
    minlambda = lambda11;
    maxlambda = lambda11;
    numIter = 1;
  }

  int signFirstStepMethod = SIGN_LAST_STEP;
  if (OPS_GetNumRemainingInputArgs() > 0) {
    const char *flag = OPS_GetString();
    if ((strcmp(flag, "-determinant") == 0) || (strcmp(flag, "-det") == 0)) {
      signFirstStepMethod = CHANGE_DETERMINANT;
    }
  }

  return new MinUnbalDispNorm(lambda11, numIter, minlambda, maxlambda,
                              signFirstStepMethod);
}




#include <SRC/analysis/integrator/Newmark1.h>
int
TclCommand_createNewmark1() {
  int numdata = OPS_GetNumRemainingInputArgs();
  if (numdata != 2 && numdata != 6) {
    opserr << "WARNING integrator Newmark1 gamma beta <alphaM> <betaKcurrent> "
              "<betaKi> <betaKlastCommitted>\n";
    return TCL_ERROR;
  }

  double data[6] = {0, 0, 0, 0, 0, 0};
  if (OPS_GetDoubleInput(&numdata, data) < 0) {
    opserr << "WARNING integrator Newmark1 invalid double inputs\n";
    return TCL_ERROR;
  }

  double gamma = data[0];
  double beta = data[1];
  double alphaM = data[2], betaK = data[3], betaKi = data[4], betaKc = data[5];

  if (numdata == 2)
    return new Newmark1(gamma, beta);
  else
    return new Newmark1(gamma, beta, alphaM, betaK, betaKi, betaKc);
}




#include <SRC/analysis/integrator/NewmarkExplicit.h>
int
TclCommand_createNewmarkExplicit(ClientData clientData, Tcl_Interp* interp, int argc, TCL_Char**const argv) {
  // pointer to an integrator that will be returned
  TransientIntegrator *theIntegrator = 0;

  int argc = OPS_GetNumRemainingInputArgs();
  if (argc != 1) {
    opserr
        << "WARNING - incorrect number of args want NewmarkExplicit $gamma\n";
    return TCL_ERROR;
  }

  double gamma;
  if (OPS_GetDouble(&argc, &gamma) != 0) {
    opserr << "WARNING - invalid args want NewmarkExplicit $gamma\n";
    return TCL_ERROR;
  }

  theIntegrator = new NewmarkExplicit(gamma);

  return theIntegrator;
}




#include <SRC/analysis/integrator/NewmarkHSFixedNumIter.h>
int
TclCommand_createNewmarkHSFixedNumIter(ClientData clientData, Tcl_Interp* interp, int argc, TCL_Char**const argv) {
  // pointer to an integrator that will be returned
  TransientIntegrator *theIntegrator = 0;

  int argc = OPS_GetNumRemainingInputArgs();
  if (argc != 2 && argc != 4) {
    opserr << "WARNING - incorrect number of args want NewmarkHSFixedNumIter "
              "$gamma $beta <-polyOrder $O>\n";
    return TCL_ERROR;
  }

  double dData[2];
  int polyOrder = 2;
  bool updDomFlag = true;
  int numData = 2;

  if (OPS_GetDouble(&numData, dData) != 0) {
    opserr << "WARNING - invalid args want NewmarkHSFixedNumIter $gamma $beta "
              "<-polyOrder $O>\n";
    return TCL_ERROR;
  }

  if (argc == 4) {
    const char *argvLoc = OPS_GetString();
    if (strcmp(argvLoc, "-polyOrder") == 0) {
      numData = 1;
      if (OPS_GetInt(&numData, &polyOrder) != 0) {
        opserr << "WARNING - invalid polyOrder want NewmarkHSFixedNumIter "
                  "$gamma $beta <-polyOrder $O>\n";
      }
    }
  }

  theIntegrator =
      new NewmarkHSFixedNumIter(dData[0], dData[1], polyOrder, updDomFlag);


  return theIntegrator;
}




#include <SRC/analysis/integrator/NewmarkHSIncrLimit.h>
int
TclCommand_createNewmarkHSIncrLimit(ClientData clientData, Tcl_Interp* interp, int argc, TCL_Char**const argv) {
  // pointer to an integrator that will be returned
  TransientIntegrator *theIntegrator = 0;

  int argc = OPS_GetNumRemainingInputArgs();
  if (argc != 3 && argc != 5) {
    opserr << "WARNING - incorrect number of args want NewmarkHSIncrLimit "
              "$gamma $beta $limit <-normType $T>\n";
    return TCL_ERROR;
  }

  double dData[3];
  int normType = 2;
  int numData = 3;

  if (OPS_GetDouble(&numData, dData) != 0) {
    opserr << "WARNING - invalid args want NewmarkHSIncrLimit $gamma $beta "
              "$limit <-normType $T>\n";
    return TCL_ERROR;
  }

  if (argc == 5) {
    const char *argvLoc = OPS_GetString();
    if (strcmp(argvLoc, "-normType") == 0) {
      numData = 1;
      if (OPS_GetInt(&numData, &normType) != 0) {
        opserr << "WARNING - invalid normType want NewmarkHSIncrLimit $gamma "
                  "$beta $limit <-normType $T>\n";
      }
    }
  }

  theIntegrator =
      new NewmarkHSIncrLimit(dData[0], dData[1], dData[2], normType);


  return theIntegrator;
}




#include <SRC/analysis/integrator/NewmarkHSIncrReduct.h>
int
TclCommand_createNewmarkHSIncrReduct(ClientData clientData, Tcl_Interp* interp, int argc, TCL_Char**const argv) {
  // pointer to an integrator that will be returned
  TransientIntegrator *theIntegrator = 0;

  int argc = OPS_GetNumRemainingInputArgs();
  if (argc != 3) {
    opserr << "WARNING - incorrect number of args want NewmarkHSIncrReduct "
              "$gamma $beta $reduct\n";
    return TCL_ERROR;
  }

  double dData[3];
  if (OPS_GetDouble(&argc, dData) != 0) {
    opserr << "WARNING - invalid args want NewmarkHSIncrReduct $gamma $beta "
              "$reduct\n";
    return TCL_ERROR;
  }

  theIntegrator = new NewmarkHSIncrReduct(dData[0], dData[1], dData[2]);


  return theIntegrator;
}




#include <SRC/analysis/integrator/Newmark.h>
int
TclCommand_createNewmark(ClientData clientData, Tcl_Interp* interp, int argc, TCL_Char**const argv) {
  // Pointer to a uniaxial material that will be returned
  TransientIntegrator *theIntegrator = 0;

  int argc = OPS_GetNumRemainingInputArgs();
  if (argc != 2 && argc != 4) {
    opserr << "WARNING - incorrect number of args want Newmark $gamma $beta "
              "<-form $typeUnknown>\n";
    return TCL_ERROR;
  }

  int dispFlag = 1;
  double dData[2];
  int numData = 2;
  if (OPS_GetDouble(&numData, dData) != 0) {
    opserr << "WARNING - invalid args want Newmark $gamma $beta <-form "
              "$typeUnknown>\n";
    return TCL_ERROR;
  }

  if (argc == 2)
    theIntegrator = new Newmark(dData[0], dData[1]);
  else {
    //    char nextString[10];
    const char *nextString = OPS_GetString();
    //    OPS_GetString(nextString, 10);
    if (strcmp(nextString, "-form") == 0) {
      //      OPS_GetString(nextString, 10);
      nextString = OPS_GetString();
      if ((nextString[0] == 'D') || (nextString[0] == 'd'))
        dispFlag = 1;
      else if ((nextString[0] == 'A') || (nextString[0] == 'a'))
        dispFlag = 3;
      else if ((nextString[0] == 'V') || (nextString[0] == 'v'))
        dispFlag = 2;
    }
    theIntegrator = new Newmark(dData[0], dData[1], dispFlag);
  }

  return theIntegrator;
}




#include <SRC/analysis/integrator/StagedLoadControl.h>
int
TclCommand_createStagedLoadControlIntegrator() {
  if (OPS_GetNumRemainingInputArgs() < 1) {
    opserr << "insufficient arguments\n";
    return TCL_ERROR;
  }

  double lambda;
  int numData = 1;
  if (OPS_GetDoubleInput(&numData, &lambda) < 0) {
    opserr << "WARNING failed to read double lambda\n";
    return TCL_ERROR;
  }

  int numIter = 1;
  double mLambda[2] = {lambda, lambda};
  if (OPS_GetNumRemainingInputArgs() > 2) {
    if (OPS_GetIntInput(&numData, &numIter) < 0) {
      opserr << "WARNING failed to read int numIter\n";
      return TCL_ERROR;
    }
    numData = 2;
    if (OPS_GetDoubleInput(&numData, &mLambda[0]) < 0) {
      opserr << "WARNING failed to read double min and max\n";
      return TCL_ERROR;
    }
  }

  return new StagedLoadControl(lambda, numIter, mLambda[0], mLambda[1]);
}
#include <tcl.h>
#include <SRC/analysis/integrator/StagedNewmark.h>

int
TclCommand_createStagedNewmark(ClientData clientData, Tcl_Interp* interp, int argc, TCL_Char**const argv) {
  // Pointer to a uniaxial material that will be returned
  TransientIntegrator *theIntegrator = 0;

  int argc = OPS_GetNumRemainingInputArgs();
  if (argc != 2 && argc != 4) {
    opserr << "WARNING - incorrect number of args want StagedNewmark $gamma "
              "$beta <-form $typeUnknown>\n";
    return TCL_ERROR;
  }

  bool dispFlag = true;
  double dData[2];
  int numData = 2;

  if (OPS_GetDouble(&numData, dData) != 0) {
    opserr << "WARNING - invalid args want StagedNewmark $gamma $beta <-form "
              "$typeUnknown>\n";
    return TCL_ERROR;
  }

  if (argc == 2)
    theIntegrator = new StagedNewmark(dData[0], dData[1]);
  else {
    //    char nextString[10];
    const char *nextString = OPS_GetString();
    //    OPS_GetString(nextString, 10);
    if (strcmp(nextString, "-form") == 0) {
      //      OPS_GetString(nextString, 10);
      nextString = OPS_GetString();
      if ((nextString[0] == 'D') || (nextString[0] == 'd'))
        dispFlag = true;
      else if ((nextString[0] == 'A') || (nextString[0] == 'a'))
        dispFlag = false;
    }
    theIntegrator = new StagedNewmark(dData[0], dData[1], dispFlag);
  }


  return theIntegrator;
}




#include <SRC/analysis/integrator/TRBDF2.h>
int
TclCommand_createTRBDF2() {
  return new TRBDF2(); 
}


#include <SRC/analysis/integrator/WilsonTheta.h>

int
TclCommand_createWilsonTheta(ClientData clientData, Tcl_Interp* interp, int argc, TCL_Char**const argv) {
  // pointer to an integrator that will be returned
  TransientIntegrator *theIntegrator = 0;

  int argc = OPS_GetNumRemainingInputArgs();
  if (argc != 1) {
    opserr << "WARNING - incorrect number of args want WilsonTheta $theta\n";
    return TCL_ERROR;
  }

  double theta;
  if (OPS_GetDouble(&argc, &theta) != 0) {
    opserr << "WARNING - invalid args want WilsonTheta $theta\n";
    return TCL_ERROR;
  }

  theIntegrator = new WilsonTheta(theta);

  return theIntegrator;
}
