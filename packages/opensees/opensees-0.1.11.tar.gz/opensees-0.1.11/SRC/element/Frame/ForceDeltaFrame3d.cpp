//===----------------------------------------------------------------------===//
//
//        OpenSees - Open System for Earthquake Engineering Simulation    
//
//===----------------------------------------------------------------------===//
//
// Higher-order frame formulations (Shear/Euler) with force/curvature interpolation
//
// References
//
//  Spacone, E., V. Ciampi, and F. C. Filippou (1996). 
//    "Mixed Formulation of Nonlinear Beam Finite Element."
//    Computers and Structures, 58(1):71-83.
//
//  Neuenhofer, A. and Filippou, F.C. (1998) 
//    "Geometrically Nonlinear Flexibility-Based Frame Finite Element", 
//    Journal of Structural Engineering, 124(6), pp. 704–711. 
//    Available at: https://doi.org/10/d8jvb5.
//
//  de Souza, R.M. (2000) 
//    "Force-based finite element for large displacement inelastic analysis of frames". 
//    University of California, Berkeley. 
//    Available at: https://www.proquest.com/docview/304624959/D8D738C3AC49427EPQ/1?accountid=14496.
//
//  Scott, M. H. (2013).
//    "Response Sensitivity of Geometrically Nonlinear Force-Based Frame Elements."
//    Journal of Structural Engineering, 139(11)
//
//  Scott, M. H. and Azad, V. J. (2017)
//    "Response sensitivity of material and geometric nonlinear force-based Timoshenko frame elements"
//    Int. J. Numer. Meth. Engng. 
//
//
// See also
//
//  Scott, M. H. and G. L. Fenves (2006). 
//    "Plastic Hinge Integration Methods for Force-Based Beam-Column Elements." 
//    Journal of Structural Engineering, 132(2):244-252.
//
//===----------------------------------------------------------------------===//
//
// Claudio Perez
//
#include <array>
#include <vector>
#include <math.h>
#include <stdlib.h>
#include <string.h>
#include <float.h>

#include <Node.h>
#include <Information.h>
#include <Parameter.h>
#include <ForceDeltaFrame3d.h>
#include <interpolate/cbdi.h>
#include <Domain.h>
#include <Channel.h>
#include <FEM_ObjectBroker.h>

#include <ElementResponse.h>
#include <BeamIntegration.h>
#include <CompositeResponse.h>
#include <ElementalLoad.h>

#define THREAD_LOCAL static
#define ELE_TAG_ForceDeltaFrame3d 0 // TODO

void
ForceDeltaFrame3d::getHk(int n, double xi[], Matrix& H)
{
  for (int i = 0; i < n; i++) {
    for (int j = 0; j < n; j++)
      H(i, j) = (pow(xi[i], j + 2) - xi[i]) / (j + 1) / (j + 2);
  }

  return;
}

void
ForceDeltaFrame3d::getHkp(int n, double xi[], Matrix& H)
{
  for (int i = 0; i < n; i++)
    for (int j = 0; j < n; j++)
      H(i, j) = pow(xi[i], j + 1) / (j + 1) - 1.0 / (j + 1) / (j + 2);
}

void
ForceDeltaFrame3d::getHg(int n, double xi[], Matrix& H)
{
  for (int i = 0; i < n; i++) {
    H(i, 0) = 0;
    for (int j = 1; j < n; j++)
      H(i, j) = (pow(xi[i], j + 1) - xi[i]) / (j + 1);
  }
}

void
ForceDeltaFrame3d::getHgp(int n, double xi[], Matrix& H)
{
  for (int i = 0; i < n; i++) {
    H(i, 0) = 0;
    for (int j = 1; j < n; j++)
      H(i, j) = pow(xi[i], j) - 1 / (j + 1);
  }
}


// constructor:
// invoked by a FEM_ObjectBroker, recvSelf() needs to be invoked on this object.
ForceDeltaFrame3d::ForceDeltaFrame3d()
 : BasicFrame3d(0, ELE_TAG_ForceDeltaFrame3d),
   stencil(nullptr),
   shear_flag(false),
   density(0.0), mass_flag(0), use_density(false),
   max_iter(0),
   tol(0.0),
   state_flag(0),
   Ki(0),
   parameterID(0)
{
  K_past.zero();
  q_past.zero();
  K_pres.zero();
  q_pres.zero();
}


ForceDeltaFrame3d::ForceDeltaFrame3d(int tag, 
                           std::array<int,2>& nodes,
                           std::vector<FrameSection*>& sections,
                           BeamIntegration& bi, 
                           FrameTransform3d& coordTransf,
                           double dens, int mass_type, bool use_mass,
                           int maxNumIters, double tolerance,
                           bool includeShear
    )
 : BasicFrame3d(tag, ELE_TAG_ForceDeltaFrame3d, nodes, coordTransf),
   stencil(nullptr),
   state_flag(0),
   Ki(nullptr),
   density(dens), mass_flag(mass_type), use_density(use_mass),
   mass_initialized(false),
   max_iter(maxNumIters), tol(tolerance),
   shear_flag(includeShear),
   parameterID(0)
{
  K_pres.zero();
  K_past.zero();
  q_past.zero();
  q_pres.zero();

  stencil = bi.getCopy();

  this->setSectionPointers(sections.size(), &sections[0]);
}


ForceDeltaFrame3d::~ForceDeltaFrame3d()
{
  for (GaussPoint& point : points)
    if (point.material != nullptr)
      delete point.material;

  if (stencil != nullptr)
    delete stencil;

  if (Ki != 0)
    delete Ki;
}

int
ForceDeltaFrame3d::setNodes()
{
  this->BasicFrame3d::setNodes();

  double L = this->getLength(State::Init);

  int numSections = points.size();
//double *xi = new double[numSections];
//double *wt = new double[numSections];
  stencil->getSectionLocations(numSections, L, xi);
  stencil->getSectionWeights(numSections, L, wt);
  for (int i=0; i<numSections; i++) {
    points[i].point  = xi[i];
    points[i].weight = wt[i];
  }
//delete[] xi;
//delete[] wt;

  if (state_flag == 0)
    this->initializeSectionHistoryVariables();

  return 0;
}

int
ForceDeltaFrame3d::commitState()
{
  int err = 0;

  // call element commitState to do any base class stuff
  if ((err = this->Element::commitState()) != 0) {
    opserr << "ForceDeltaFrame3d::commitState () - failed in base class";
    return err;
  }

  for (GaussPoint& point : points) {
    point.es_save = point.es;
    if (point.material->commitState() != 0)
      return -1;
  } 

  // commit the transformation between coord. systems
  if ((err = theCoordTransf->commitState()) != 0)
    return err;

  // commit the element variables state
  K_past = K_pres;
  q_past = q_pres;

  //   state_flag = 0;  fmk - commented out, see what happens to Example3.1.tcl if uncommented
  //                         - i have not a clue why, ask remo if he ever gets in contact with us again!

  return err;
}

int
ForceDeltaFrame3d::revertToLastCommit()
{

  for (GaussPoint& point : points) {
    FrameSection& section = *point.material;

    point.es = point.es_save;

    if (section.revertToLastCommit() != 0)
      return -1;

    section.setTrialState<nsr,scheme>(point.es);
    point.sr = section.getResultant<nsr,scheme>();
    point.Fs = section.getFlexibility<nsr,scheme>();
  }


  // Revert the transformation to last commit
  if (theCoordTransf->revertToLastCommit() != 0)
    return -2;

  // revert the element state to last commit
  q_pres = q_past;
  K_pres = K_past;

  state_flag = 0;

  return 0;
}

int
ForceDeltaFrame3d::revertToStart()
{
  // Revert the transformation to start
  if (theCoordTransf->revertToStart() != 0)
    return -2;

  // Loop over the integration points and revert states to start
  for (GaussPoint& point : points) {
    point.Fs.zero();
    point.es.zero();
    point.sr.zero();
    point.es_save.zero();
    if (point.material->revertToStart() != 0)
      return -1;
  }

  // revert the element state to start
  q_past.zero();
  K_past.zero();

  q_pres.zero();
  K_pres.zero();

  state_flag = 0;
  // this->update();
  return 0;
}



void
ForceDeltaFrame3d::initializeSectionHistoryVariables()
{
  for (int i = 0; i < points.size(); i++) {
    points[i].Fs.zero();
    points[i].es.zero();
    points[i].sr.zero();
    points[i].es_save.zero();
  }
}



int
ForceDeltaFrame3d::update()
{
  const int nip = points.size();

  // TODO: remove hard limit on sections
  THREAD_LOCAL VectorND<nsr>     es_trial[maxNumSections]; //  strain
  THREAD_LOCAL VectorND<nsr>     sr_trial[maxNumSections]; //  stress resultant
  THREAD_LOCAL MatrixND<nsr,nsr> Fs_trial[maxNumSections]; //  flexibility

  // if have completed a recvSelf() - do a revertToLastCommit
  // to get sr, etc. set correctly
  if (state_flag == 2)
    this->revertToLastCommit();

  // update the transformation
  theCoordTransf->update();

  // get basic displacements and increments
  const Vector& v = theCoordTransf->getBasicTrialDisp();

  THREAD_LOCAL VectorND<nq> dv{0.0};
  dv = theCoordTransf->getBasicIncrDeltaDisp();

  if (state_flag != 0 && dv.norm() <= DBL_EPSILON && eleLoads.size() == 0)
    return 0;

  THREAD_LOCAL VectorND<nq> Dv;
  Dv = v;
  Dv -= dv;

  double L        = theCoordTransf->getInitialLength();
  double oneOverL = 1.0 / L;


  static VectorND<nq>    dv_trial;
  static VectorND<nq>    q_trial;
  static MatrixND<nq,nq> K_trial;
  
  dv_trial = dv;
  q_trial  = q_pres;
  K_trial  = K_pres;

  for (int i = 0; i < points.size(); i++) {
    es_trial[i] = points[i].es;
    Fs_trial[i] = points[i].Fs;
    sr_trial[i] = points[i].sr;
  }


  Vector stilde(nsr * points.size());
  for (int i = 0; i < points.size(); i++) {
    auto s = points[i].material->getResultant<nsr,scheme>();
    for (int j = 0; j < nsr; j++)
      stilde(nsr*i + j) = s[j];
  }

  // Get CBDI influence matrix
  Matrix ls(nip, nip);
  // getCBDIinfluenceMatrix(nip, xi, L, ls);
  Matrix lsgp(nip, nip);
  Matrix lskp(nip, nip);

  Matrix G(nip, nip);
  vandermonde(nip, xi, G);


  Matrix Hk(nip, nip);
  Matrix& lsg = Hk;

  {
    Matrix Ginv(nip, nip);
    G.Invert(Ginv);

    this->getHk(nip, xi, Hk);

    ls.addMatrixProduct(0.0, Hk, Ginv, 1.0);

    Matrix Hg(nip, nip);
    this->getHg(nip, xi, Hg);

    Hk.addMatrixProduct(0.0, Hg, Ginv, 1.0);
    Matrix Hkp(nip, nip);
    this->getHkp(nip, xi, Hkp);
    lskp.addMatrixProduct(0.0, Hkp, Ginv, 1.0);

    Matrix Hgp(nip, nip);
    this->getHgp(nip, xi, Hgp);
    lsgp.addMatrixProduct(0.0, Hgp, Ginv, 1.0);
  }

  static VectorND<nq>    dq_trial;
  static VectorND<nq>    vr;       // element residual displacements
  static MatrixND<nq,nq> F;        // Element flexibility

  // calculate nodal force increments and update nodal forces
  // dq_trial = kv * dv;
  dq_trial.addMatrixVector(0.0, K_trial, dv_trial, 1.0);

  Vector gamma(nip);
  Vector gammaz(nip);
  Vector kappa(nip);
  Vector kappay(nip);

  Vector w(nip);
  Vector wp(nip);
  Vector wz(nip);
  Vector wpz(nip);
  Vector ds_tilde(nsr * nip);
  Matrix K_tilde(nsr * nip, nsr * nip);
  Vector de_tilde(nsr * nip);


  bool converged   = false;
  for (int j = 0; j < max_iter; j++) {

    q_trial += dq_trial;

    // initialize F and vr for integration
    F.zero();
    vr.zero();

    //
    // Preliminary Gauss Loop
    //
    for (int i = 0; i < nip; i++) {
      kappa(i)  = 0.0;
      gamma(i)  = 0.0;
      kappay(i) = 0.0;
      gammaz(i) = 0.0;
      for (int j = 0; j < nsr; j++) {
        if (scheme[j] == SECTION_RESPONSE_VY)
          gamma(i) += es_trial[i][j];
        if (scheme[j] == SECTION_RESPONSE_VZ)
          gammaz(i) += es_trial[i][j];
        if (scheme[j] == SECTION_RESPONSE_MY)
          kappay(i) += es_trial[i][j];
        if (scheme[j] == SECTION_RESPONSE_MZ)
          kappa(i) += es_trial[i][j];
      }
    }

    w.addMatrixVector(0.0, ls, kappa, L * L);
    if (shear_flag) {
      w.addMatrixVector(1.0, lsg, gamma, L);
      wp.addMatrixVector(0.0, lskp, kappa, L);
      wp.addMatrixVector(1.0, lsgp, gamma, 1.0);
    }

    wz.addMatrixVector(0.0, ls, kappay, L * L);
    if (shear_flag) {
      wz.addMatrixVector(1.0, lsg, gammaz, L);
      wpz.addMatrixVector(0.0, lskp, kappay, L);
      wpz.addMatrixVector(1.0, lsgp, gammaz, 1.0);
    }

    //
    // Gauss Loop
    //
    for (int i = 0; i < nip; i++) {

      int index = nsr * i;
      double xL = points[i].point;

      FrameSection& section = *points[i].material;

      //
      // a. Calculate interpolated section force
      //
      //    si = B*q + Bp*w;
      //
      for (int j = 0; j < nsr; j++) {

        if (scheme[j] == SECTION_RESPONSE_P)
          ds_tilde(index) = q_trial[0] - stilde(index);
        if (scheme[j] == SECTION_RESPONSE_VY)
          ds_tilde(index) =  -wp(i) * q_trial[0] - oneOverL * (q_trial[1] + q_trial[2]) - stilde(index);
        if (scheme[j] == SECTION_RESPONSE_VZ)
          ds_tilde(index) = -wpz(i) * q_trial[0] - oneOverL * (q_trial[3] + q_trial[4]) - stilde(index);
        if (scheme[j] == SECTION_RESPONSE_T)
          ds_tilde(index) = q_trial[5] - stilde(index);
        if (scheme[j] == SECTION_RESPONSE_MY)
          ds_tilde(index) =  wz(i) * q_trial[0] + (xL - 1) * q_trial[3] + xL * q_trial[4] - stilde(index);
        if (scheme[j] == SECTION_RESPONSE_MZ)
          ds_tilde(index) =   w(i) * q_trial[0] + (xL - 1) * q_trial[1] + xL * q_trial[2] - stilde(index);
        index++;
      }

      // Add the effects of element loads
      // si += bp*w
      //
      if (eleLoads.size() > 0) {
        VectorND<nsr> sp{0.0};
        this->computeSectionForces(sp, i);
        for (int ii = 0; ii < nsr; ii++)
          ds_tilde(nsr*i + ii) += sp[ii];
      }
    } // Section loop

    //
    K_tilde.Zero();
    for (int i = 0; i < nip; i++) {
      Fs_trial[i] = points[i].material->getFlexibility<nsr,scheme>();
      const MatrixND<nsr,nsr> Ks = points[i].material->getTangent<nsr,scheme>(State::Pres);


      for (int j = 0; j < nip; j++) {
        for (int k = 0; k < nsr; k++) {
          if (shear_flag && scheme[k] == SECTION_RESPONSE_VY) {
            K_tilde(nsr*i + k, nsr*j + k)     -= lsgp(i, j) * q_trial[0];
            for (int l=0; l< nsr; l++)
              if (scheme[l] == SECTION_RESPONSE_MZ)
                K_tilde(nsr*i + k, nsr*j + l) -= lskp(i, j) * L * q_trial[0];
          }
          if (shear_flag && scheme[k] == SECTION_RESPONSE_VZ) {
            K_tilde(nsr*i + k, nsr*j + k) -= lsgp(i, j) * q_trial[0];
            for (int l=0; l< nsr; l++)
              if (scheme[l] == SECTION_RESPONSE_MY)
                K_tilde(nsr*i + k, nsr*j + l) -= lskp(i, j) * L * q_trial[0];
          }

          if (scheme[k] == SECTION_RESPONSE_MY) {
            K_tilde(nsr*i + k, nsr*j + k) += ls(i, j) * L * L * q_trial[0];
            for (int l=0; l< nsr; l++)
              if (shear_flag && scheme[l] == SECTION_RESPONSE_VZ)
                K_tilde(nsr*i + k, nsr*j + l) += lsg(i, j) * L * q_trial[0];
          }
          if (scheme[k] == SECTION_RESPONSE_MZ) {
            K_tilde(nsr*i + k, nsr*j + k) += ls(i, j) * L * L * q_trial[0];
            for (int l=0; l< nsr; l++)
              if (shear_flag && scheme[l] == SECTION_RESPONSE_VY)
                K_tilde(nsr*i + k, nsr*j + l) += lsg(i, j) * L * q_trial[0];
          }
        }
      }
      for (int ii = 0; ii < nsr; ii++)
        for (int jj = 0; jj < nsr; jj++)
          K_tilde(nsr*i + ii, nsr*i + jj) -= Ks(ii, jj);
    }

    K_tilde.Solve(ds_tilde, de_tilde);

    for (int i = 0; i < nip; i++) {
      for (int k = 0; k < nsr; k++)
        es_trial[i][k] -= de_tilde(nsr*i + k);
    }

    for (int i = 0; i < nip; i++) {
      kappa(i)  = 0.0;
      gamma(i)  = 0.0;
      kappay(i) = 0.0;
      gammaz(i) = 0.0;
      for (int k = 0; k < nsr; k++) {
        if (scheme[k] == SECTION_RESPONSE_VY)
          gamma(i) += es_trial[i][k];
        if (scheme[k] == SECTION_RESPONSE_VZ)
          gammaz(i) += es_trial[i][k];
        if (scheme[k] == SECTION_RESPONSE_MY)
          kappay(i) += es_trial[i][k];
        if (scheme[k] == SECTION_RESPONSE_MZ)
          kappa(i) += es_trial[i][k];
      }
    }

    w.addMatrixVector(0.0, ls, kappa, L * L);
    if (shear_flag) {
       w.addMatrixVector(1.0, lsg,  gamma, L);
      wp.addMatrixVector(0.0, lskp, kappa, L);
      wp.addMatrixVector(1.0, lsgp, gamma, 1.0);
    }
    wz.addMatrixVector(0.0, ls, kappay, L * L);
    if (shear_flag) {
      wz.addMatrixVector(1.0, lsg, gammaz, L);
      wpz.addMatrixVector(0.0, lskp, kappay, L);
      wpz.addMatrixVector(1.0, lsgp, gammaz, 1.0);
    }

    //
    //
    //
    K_tilde.Zero();
    for (int i = 0; i < nip; i++) {

      points[i].material->setTrialState<nsr,scheme>(es_trial[i]);

      sr_trial[i] = points[i].material->getResultant<nsr, scheme>();
      Fs_trial[i] = points[i].material->getFlexibility<nsr,scheme>();
      const MatrixND<nsr,nsr> Ks = points[i].material->getTangent<nsr,scheme>(State::Pres);


      double xL = points[i].point;

      int index = nsr * i;
      for (int j = 0; j < nsr; j++) {

        if (scheme[j] == SECTION_RESPONSE_P)
          ds_tilde(index) = q_trial[0];
        if (scheme[j] == SECTION_RESPONSE_VY)
          ds_tilde(index) = -wp(i) * q_trial[0] - oneOverL * (q_trial[1] + q_trial[2]);
        if (scheme[j] == SECTION_RESPONSE_VZ)
          ds_tilde(index) = -wpz(i) * q_trial[0] - oneOverL * (q_trial[3] + q_trial[4]);
        if (scheme[j] == SECTION_RESPONSE_T)
          ds_tilde(index) = q_trial[5];
        if (scheme[j] == SECTION_RESPONSE_MZ)
          ds_tilde(index) = w(i) * q_trial[0] + (xL - 1.0) * q_trial[1] + xL * q_trial[2];
        if (scheme[j] == SECTION_RESPONSE_MY)
          ds_tilde(index) = wz(i) * q_trial[0] + (xL - 1.0) * q_trial[3] + xL * q_trial[4];

        ds_tilde(index) -= sr_trial[i][j];

        index++;
      }

      if (eleLoads.size() > 0) {
        VectorND<nsr> sp{0.0};
        this->computeSectionForces(sp, i);
        for (int ii = 0; ii < nsr; ii++) {
          ds_tilde(nsr*i + ii) += sp[ii];
        }
      }

      for (int j = 0; j < nip; j++) {
        for (int k = 0; k < nsr; k++) {
          if (shear_flag && scheme[k] == SECTION_RESPONSE_VY) {
            K_tilde(nsr*i + k, nsr*j + k)     -= lsgp(i, j) * q_trial[0];
            for (int l=0; l< nsr; l++)
              if (scheme[l] == SECTION_RESPONSE_MZ)
                K_tilde(nsr*i + k, nsr*j + l) -= lskp(i, j) * L * q_trial[0];
          }
          if (shear_flag && scheme[k] == SECTION_RESPONSE_VZ) {
            K_tilde(nsr*i + k, nsr*j + k) -= lsgp(i, j) * q_trial[0];
            for (int l=0; l< nsr; l++)
              if (scheme[l] == SECTION_RESPONSE_MY)
                K_tilde(nsr*i + k, nsr*j + l) -= lskp(i, j) * L * q_trial[0];
          }

          if (scheme[k] == SECTION_RESPONSE_MY) {
            K_tilde(nsr*i + k, nsr*j + k) += ls(i, j) * L * L * q_trial[0];
            for (int l=0; l< nsr; l++)
              if (shear_flag && scheme[l] == SECTION_RESPONSE_VZ)
                K_tilde(nsr*i + k, nsr*j + l) += lsg(i, j) * L * q_trial[0];
          }
          if (scheme[k] == SECTION_RESPONSE_MZ) {
            K_tilde(nsr*i + k, nsr*j + k) += ls(i, j) * L * L * q_trial[0];
            for (int l=0; l< nsr; l++)
              if (shear_flag && scheme[l] == SECTION_RESPONSE_VY)
                K_tilde(nsr*i + k, nsr*j + l) += lsg(i, j) * L * q_trial[0];
          }
        }
      }
      for (int ii = 0; ii < nsr; ii++)
        for (int jj = 0; jj < nsr; jj++)
          K_tilde(nsr*i + ii, nsr*i + jj) -= Ks(ii, jj);

    } // Primary section loop

    //
    //
    //
    K_tilde.Solve(ds_tilde, de_tilde);

    for (int i = 0; i < nip; i++) {
      for (int j = 0; j < nsr; j++)
        es_trial[i][j] -= de_tilde(nsr*i + j);
    }

    for (int i = 0; i < nip; i++) {
      kappa(i)  = 0.0;
      gamma(i)  = 0.0;
      kappay(i) = 0.0;
      gammaz(i) = 0.0;
      for (int j = 0; j < nsr; j++) {
        if (scheme[j] == SECTION_RESPONSE_VY)
          gamma(i) += es_trial[i][j];
        if (scheme[j] == SECTION_RESPONSE_VZ)
          gammaz(i) += es_trial[i][j];
        if (scheme[j] == SECTION_RESPONSE_MY)
          kappay(i) += es_trial[i][j];
        if (scheme[j] == SECTION_RESPONSE_MZ)
          kappa(i) += es_trial[i][j];
      }
    }

    w.addMatrixVector(0.0, ls, kappa, L * L);
    if (shear_flag) {
      w.addMatrixVector(1.0, lsg, gamma, L);
      wp.addMatrixVector(0.0, lskp, kappa, L);
      wp.addMatrixVector(1.0, lsgp, gamma, 1.0);
    }
    wz.addMatrixVector(0.0, ls, kappay, L * L);
    if (shear_flag) {
      wz.addMatrixVector(1.0, lsg, gammaz, L);
      wpz.addMatrixVector(0.0, lskp, kappay, L);
      wpz.addMatrixVector(1.0, lsgp, gammaz, 1.0);
    }


    // Form stilde
    for (int i = 0; i < nip; i++) {
      int index = nsr * i;
      for (int j = 0; j < nsr; j++) {
        if (scheme[j] == SECTION_RESPONSE_P)
          stilde(index) = q_trial[0];
        if (scheme[j] == SECTION_RESPONSE_VY)
          stilde(index) = -wp(i) * q_trial[0] - oneOverL * (q_trial[1] + q_trial[2]);
        if (scheme[j] == SECTION_RESPONSE_VZ)
          stilde(index) = -wp(i) * q_trial[0] - oneOverL * (q_trial[3] + q_trial[4]);
        if (scheme[j] == SECTION_RESPONSE_T)
          stilde(index) = q_trial[5];
        if (scheme[j] == SECTION_RESPONSE_MZ)
          stilde(index) = w(i) * q_trial[0] + (xi[i] - 1) * q_trial[1] + xi[i] * q_trial[2];
        if (scheme[j] == SECTION_RESPONSE_MY)
          stilde(index) = w(i) * q_trial[0] + (xi[i] - 1) * q_trial[3] + xi[i] * q_trial[4];

        index++;
      }

      if (eleLoads.size() > 0) {
        VectorND<nsr> sp{0.0};
        this->computeSectionForces(sp, i);
        for (int ii = 0; ii < nsr; ii++)
          stilde(nsr*i + ii) += sp[ii];
      }
    } // loop over sections

    Matrix dwidq(2 * nip, nq);
    this->computedwdq(dwidq, q_trial, w, wp, ls, lsg, lskp, lsgp);
    Matrix dwzidq(2 * nip, nq);
    this->computedwzdq(dwzidq, q_trial, wz, wpz, ls, lsg, lskp, lsgp);

    //
    //
    //
    MatrixND<nsr, nq> Bstr{0};
    MatrixND<nsr, nq> Bhat{0};
    for (int i = 0; i < nip; i++) {
      double xL = points[i].point;
      double wtL = points[i].weight * L;

      for (int j = 0; j < nsr; j++) {
        if (scheme[j] == SECTION_RESPONSE_P) {
          Bstr(j, 0) = 1.0;
          Bhat(j, 0) = 1.0;
        }
        if (scheme[j] == SECTION_RESPONSE_MZ) {
          Bstr(j, 0) = 0.5 * w(i);
          Bstr(j, 1) = xL - 1;
          Bstr(j, 2) = xL;

          Bhat(j, 0) = w(i);
          Bhat(j, 1) = xL - 1;
          Bhat(j, 2) = xL;
        }
        if (scheme[j] == SECTION_RESPONSE_VY) {
          Bstr(j, 0) = -0.5 * wp(i);
          Bstr(j, 1) = -oneOverL;
          Bstr(j, 2) = -oneOverL;

          Bhat(j, 0) = -wp(i);
          Bhat(j, 1) = -oneOverL;
          Bhat(j, 2) = -oneOverL;
        }
        if (scheme[j] == SECTION_RESPONSE_MY) {
          Bstr(j, 0) = 0.5 * wz(i);
          Bstr(j, 3) = xL - 1;
          Bstr(j, 4) = xL;

          Bhat(j, 0) = wz(i);
          Bhat(j, 3) = xL - 1;
          Bhat(j, 4) = xL;
        }
        if (scheme[j] == SECTION_RESPONSE_VZ) {
          Bstr(j, 0) = -0.5 * wpz(i);
          Bstr(j, 3) = -oneOverL;
          Bstr(j, 4) = -oneOverL;

          Bhat(j, 0) = -wpz(i);
          Bhat(j, 3) = -oneOverL;
          Bhat(j, 4) = -oneOverL;
        }
        if (scheme[j] == SECTION_RESPONSE_T) {
          Bstr(j, 5) = 1.0;
          Bhat(j, 5) = 1.0;
        }
      }

      MatrixND<nsr,nsr> &fSec = Fs_trial[i]; /// points[i].material->getFlexibility<nsr,scheme>();

      // F = F + Bstr' (fSec * Bhat) * wtL;
      F.addMatrixTripleProduct(1.0, Bstr, fSec, Bhat, wtL);

      // F = F + Bstr' fsec * (dbdw * q * dwdq) * wtL;
      Bhat.zero();
      for (int j = 0; j < nsr; j++) {
        if (scheme[j] == SECTION_RESPONSE_MZ)
          for (int k = 0; k < nq; k++)
            Bhat(j, k) = q_trial[0] * dwidq(i, k);
        if (scheme[j] == SECTION_RESPONSE_MY)
          for (int k = 0; k < nq; k++)
            Bhat(j, k) = q_trial[0] * dwzidq(i, k);
      }
      F.addMatrixTripleProduct(1.0, Bstr, fSec, Bhat, wtL);
      Bhat.zero();
      for (int j = 0; j < nsr; j++) {
        if (scheme[j] == SECTION_RESPONSE_VY)
          for (int k = 0; k < nq; k++)
            Bhat(j, k) = -q_trial[0] * dwidq(i + nip, k);
        if (scheme[j] == SECTION_RESPONSE_VZ)
          for (int k = 0; k < nq; k++)
            Bhat(j, k) = -q_trial[0] * dwzidq(i + nip, k);
      }
      F.addMatrixTripleProduct(1.0, Bstr, fSec, Bhat, wtL);

      // F = F + dBstr/dw ^ (e * dwdq) * wtL
      const VectorND<nsr>& e = es_trial[i];
      for (int j = 0; j < nsr; j++) {
        if (scheme[j] == SECTION_RESPONSE_MZ)
          for (int k = 0; k < nq; k++)
            F(0, k) += 0.5 * e[j] * dwidq(i, k) * wtL;
        if (scheme[j] == SECTION_RESPONSE_VY)
          for (int k = 0; k < nq; k++)
            F(0, k) -= 0.5 * e[j] * dwidq(i + nip, k) * wtL;
        if (scheme[j] == SECTION_RESPONSE_MY)
          for (int k = 0; k < nq; k++)
            F(0, k) += 0.5 * e[j] * dwzidq(i, k) * wtL;
        if (scheme[j] == SECTION_RESPONSE_VZ)
          for (int k = 0; k < nq; k++)
            F(0, k) -= 0.5 * e[j] * dwzidq(i + nip, k) * wtL;
      }


      //
      // Integrate residual deformations
      //
      // vr += (b^ (vs + dvs)) * wtL;
      //
      //vr.addMatrixTransposeVector(1.0, b[i], points[i].es + dvs, wtL);
      //dvs.addVector(1.0, es_trial[i], 1.0);
      const VectorND<nsr>& des = es_trial[i];
      double tmp;
      for (int ii = 0; ii < nsr; ii++) {
        double dei = des[ii] * wtL;
        switch (scheme[ii]) {
        case SECTION_RESPONSE_P:
          vr[0] += dei;
          break;
        case SECTION_RESPONSE_VY:
          tmp = oneOverL * dei;
          vr[0] -= 0.5 * wp(i) * dei;
          vr[1] -= tmp;
          vr[2] -= tmp;
          break;
        case SECTION_RESPONSE_VZ:
          tmp = oneOverL * dei;
          vr[0] -= 0.5 * wpz(i) * dei;
          vr[3] -= tmp;
          vr[4] -= tmp;
          break;
        case SECTION_RESPONSE_T:
          vr[5] += dei;
          break;
        case SECTION_RESPONSE_MY:
          vr[0] += 0.5 * wz(i) * dei;
          vr[3] += (xL - 1) * dei;
          vr[4] += xL * dei;
          break;
        case SECTION_RESPONSE_MZ:
          vr[0] += 0.5 * w(i) * dei;
          vr[1] += (xL - 1.0) * dei;
          vr[2] += xL * dei;
          break;
        default:
          break;
        }
      }
    }

    // dv = Dv + dv_trial  - vr

    dv = v;
    dv -= vr;

    // dq_trial = kv * dv;
    dq_trial.addMatrixVector(0.0, K_trial, dv, 1.0);

    double dW = dq_trial.dot(dv);

    // check for convergence of this interval
    if (fabs(dW) < tol)
      break;

  } // For iteration


  // Calculate element stiffness matrix
  if (F.invert(K_trial) < 0)
    opserr << "ForceDeltaFrame3d::update() -- could not invert flexibility\n";


  K_pres = K_trial;
  q_pres = q_trial;
  for (int k = 0; k < nip; k++) {
    points[k].es  = es_trial[k];
    points[k].Fs  = Fs_trial[k];
    points[k].sr  = sr_trial[k];
  }

  state_flag = 1;

  return 0;
}


const Vector &
ForceDeltaFrame3d::getResistingForce()
{
 
  double q0 = q_pres[0];
  double q1 = q_pres[1];
  double q2 = q_pres[2];
  double q3 = q_pres[3];
  double q4 = q_pres[4];
  double q5 = q_pres[5];

  double oneOverL = 1.0 / theCoordTransf->getInitialLength();

  thread_local VectorND<12> pl;
  pl[0]  = -q0;                    // Ni
  pl[1]  =  oneOverL * (q1 + q2);  // Viy
  pl[2]  = -oneOverL * (q3 + q4);  // Viz
  pl[3]  = -q5;                    // Ti
  pl[4]  =  q3;
  pl[5]  =  q1;
  pl[6]  =  q0;                    // Nj
  pl[7]  = -pl[1];                 // Vjy
  pl[8]  = -pl[2];                 // Vjz
  pl[9]  = q5;                     // Tj
  pl[10] = q4;
  pl[11] = q2;

  // Push to global system
  thread_local VectorND<12> pg;
  thread_local Vector wrapper(pg);

  pg  = theCoordTransf->pushResponse(pl);

  // Add loading
  double p0[5]{};
  if (eleLoads.size() > 0) // (eleLoads.size() > 0)
    this->computeReactions(p0);

  thread_local VectorND<12> pf{0.0};
  pf[0] = p0[0];
  pf[1] = p0[1];
  pf[7] = p0[2];
  pf[2] = p0[3];
  pf[8] = p0[4];

  pg += theCoordTransf->pushConstant(pf);
//if (total_mass != 0.0)
//  wrapper.addVector(1.0, p_iner, -1.0);

  return wrapper;
}

const Matrix &
ForceDeltaFrame3d::getTangentStiff()
{
  MatrixND<nq,nq> kb = this->getBasicTangent(State::Pres, 0);

  double q0 = q_pres[0];
  double q1 = q_pres[1];
  double q2 = q_pres[2];
  double q3 = q_pres[3];
  double q4 = q_pres[4];
  double q5 = q_pres[5];

  double oneOverL = 1.0 / theCoordTransf->getInitialLength();

  THREAD_LOCAL VectorND<12> pl{0.0};
  pl[0]  = -q0;                    // Ni
  pl[1]  =  oneOverL * (q1 + q2);  // Viy
  pl[2]  = -oneOverL * (q3 + q4);  // Viz
  pl[3]  = -q5;                    // Ti
  pl[4]  =  q3;
  pl[5]  =  q1;
  pl[6]  =  q0;                    // Nj
  pl[7]  = -pl[1];                 // Vjy
  pl[8]  = -pl[2];                 // Vjz
  pl[9]  =  q5;                    // Tj
  pl[10] =  q4;
  pl[11] =  q2;
  

  // Transform basic stiffness to local system
  THREAD_LOCAL double tmp[12][12]{};  // Temporary storage
  // First compute kb*T_{bl}
  for (int i = 0; i < 6; i++) {
    tmp[i][ 0] = -kb(i, 0);
    tmp[i][ 1] =  oneOverL * (kb(i, 1) + kb(i, 2));
    tmp[i][ 2] = -oneOverL * (kb(i, 3) + kb(i, 4));
    tmp[i][ 3] = -kb(i, 5);
    tmp[i][ 4] =  kb(i, 3);
    tmp[i][ 5] =  kb(i, 1);
    tmp[i][ 6] =  kb(i, 0);
    tmp[i][ 7] = -tmp[i][1];
    tmp[i][ 8] = -tmp[i][2];
    tmp[i][ 9] =  kb(i, 5);
    tmp[i][10] =  kb(i, 4);
    tmp[i][11] =  kb(i, 2);
  }

  THREAD_LOCAL MatrixND<12,12> kl{0.0};  // Local stiffness
  // Now compute T'_{bl}*(kb*T_{bl})
  for (int i = 0; i < 12; i++) {
    kl( 0, i) = -tmp[0][i];
    kl( 1, i) =  oneOverL * (tmp[1][i] + tmp[2][i]);
    kl( 2, i) = -oneOverL * (tmp[3][i] + tmp[4][i]);
    kl( 3, i) = -tmp[5][i];
    kl( 4, i) = tmp[3][i];
    kl( 5, i) = tmp[1][i];
    kl( 6, i) = tmp[0][i];
    kl( 7, i) = -kl(1, i);
    kl( 8, i) = -kl(2, i);
    kl( 9, i) = tmp[5][i];
    kl(10, i) = tmp[4][i];
    kl(11, i) = tmp[2][i];
  }


  THREAD_LOCAL MatrixND<12,12> Kg;
  THREAD_LOCAL Matrix Wrapper(Kg);
  Kg = theCoordTransf->pushResponse(kl, pl);
  return Wrapper;
}



void
ForceDeltaFrame3d::computew(Vector& w, Vector& wp, double xi[], const Vector& kappa, const Vector& gamma)
{
  int numSections = points.size();
  double L = theCoordTransf->getInitialLength();


  Matrix Ginv(numSections, numSections);
  vandermonde_inverse(numSections, xi, Ginv);


  bool isGamma = false;
  for (int i = 0; i < numSections; i++) {
    if (gamma[i] != 0.0)
      isGamma = true;
  }
  isGamma = shear_flag && isGamma;

  Matrix H(numSections, numSections);
  Matrix ls(numSections, numSections);

  this->getHk(numSections, xi, H);
  ls.addMatrixProduct(0.0, H, Ginv, 1.0);
  w.addMatrixVector(0.0, ls, kappa, L * L);

  if (isGamma) {
    this->getHg(numSections, xi, H);
    ls.addMatrixProduct(0.0, H, Ginv, 1.0);
    w.addMatrixVector(1.0, ls, gamma, L);

    this->getHkp(numSections, xi, H);
    ls.addMatrixProduct(0.0, H, Ginv, 1.0);
    wp.addMatrixVector(0.0, ls, kappa, L);

    this->getHgp(numSections, xi, H);
    ls.addMatrixProduct(0.0, H, Ginv, 1.0);
    wp.addMatrixVector(1.0, ls, gamma, 1.0);
  }
}

void
ForceDeltaFrame3d::computedwdq(Matrix& dwidq, 
                               const Vector& q, 
                               const Vector& w,    const Vector& wp,
                               const Matrix& lsk,  const Matrix& lsg, 
                               const Matrix& lskp, const Matrix& lsgp)
{
  int numSections = points.size();
  double L        = theCoordTransf->getInitialLength();
  double oneOverL = 1.0 / L;

  Matrix A(2 * numSections, 2 * numSections);
  Matrix b(2 * numSections, nq);

  Matrix Fksb(numSections, nq);
  Matrix Fgsb(numSections, nq);

  bool isGamma = false;

  for (int i = 0; i < numSections; i++) {

    const MatrixND<nsr,nsr> Fs = points[i].material->getFlexibility<nsr,scheme>();

    double FkM = 0.0;
    double FgM = 0.0;
    double FkV = 0.0;
    double FgV = 0.0;

    for (int j = 0; j < nsr; j++) {

      if (scheme[j] == SECTION_RESPONSE_MZ) {
        FkM += Fs(j, j);

        for (int k = 0; k < nsr; k++) {
          if (scheme[k] == SECTION_RESPONSE_P)
            Fksb(i, 0) += Fs(j, k);
          if (scheme[k] == SECTION_RESPONSE_MZ) {
            Fksb(i, 0) += w(i) * Fs(j, k);
            Fksb(i, 1) += (xi[i] - 1) * Fs(j, k);
            Fksb(i, 2) += xi[i] * Fs(j, k);
          }
          if (scheme[k] == SECTION_RESPONSE_VY) {
            FkV += Fs(j, k);

            Fksb(i, 0) -= wp(i) * Fs(j, k);
            Fksb(i, 1) -= oneOverL * Fs(j, k);
            Fksb(i, 2) -= oneOverL * Fs(j, k);
          }
        }
      }
      if (scheme[j] == SECTION_RESPONSE_VY) {
        isGamma = true;
        FgV += Fs(j, j);

        for (int k = 0; k < nsr; k++) {
          if (scheme[k] == SECTION_RESPONSE_P)
            Fgsb(i, 0) += Fs(j, k);
          if (scheme[k] == SECTION_RESPONSE_MZ) {
            FgM += Fs(j, k);

            Fgsb(i, 0) += w(i) * Fs(j, k);
            Fgsb(i, 1) += (xi[i] - 1) * Fs(j, k);
            Fgsb(i, 2) += xi[i] * Fs(j, k);
          }
          if (scheme[k] == SECTION_RESPONSE_VY) {
            Fgsb(i, 0) -= wp(i) * Fs(j, k);
            Fgsb(i, 1) -= oneOverL * Fs(j, k);
            Fgsb(i, 2) -= oneOverL * Fs(j, k);
          }
        }
      }
    }

    isGamma = shear_flag && isGamma;

    A(i, i)                             = 1.0;
    A(i + numSections, i + numSections) = 1.0;

    double q1 = q(0);

    for (int j = 0; j < numSections; j++) {
      A(j, i) -= q1 * L * L * FkM * lsk(j, i);
      if (isGamma) {
        A(j, i) -= q1 * L * FgM * lsg(j, i);

        A(j, i + numSections) += q1 * L * L * FkV * lsk(j, i);
        A(j, i + numSections) += q1 * L * FgV * lsg(j, i);

        A(j + numSections, i) -= q1 * L * FkM * lskp(j, i);
        A(j + numSections, i) -= q1 * FgM * lsgp(j, i);

        A(j + numSections, i + numSections) += q1 * L * FkV * lskp(j, i);
        A(j + numSections, i + numSections) += q1 * FgV * lsgp(j, i);
      }
    }
  }

  Matrix mhs(numSections, nq);

  mhs.addMatrixProduct(0.0, lsk, Fksb, L * L);
  if (isGamma)
    mhs.addMatrixProduct(1.0, lsg, Fgsb, L);

  for (int i = 0; i < numSections; i++)
    for (int j = 0; j < nq; j++)
      b(i, j) = mhs(i, j);

  if (isGamma) {
    mhs.addMatrixProduct(0.0, lskp, Fksb, L);
    mhs.addMatrixProduct(1.0, lsgp, Fgsb, 1.0);
    for (int i = 0; i < numSections; i++)
      for (int j = 0; j < nq; j++)
        b(i + numSections, j) = mhs(i, j);
  }

  A.Solve(b, dwidq);

  return;
}

void
ForceDeltaFrame3d::computedwzdq(Matrix& dwzidq, const Vector& q, const Vector& wz, const Vector& wpz,
                           const Matrix& lsk, const Matrix& lsg, const Matrix& lskp,
                           const Matrix& lsgp)
{
  int numSections = points.size();
  double L        = theCoordTransf->getInitialLength();
  double oneOverL = 1.0 / L;

  Matrix A(2 * numSections, 2 * numSections);
  Matrix b(2 * numSections, nq);

  Matrix Fksb(numSections, nq);
  Matrix Fgsb(numSections, nq);

  bool isGamma = false;

  for (int i = 0; i < numSections; i++) {

    MatrixND<nsr,nsr> Fs = points[i].material->getFlexibility<nsr,scheme>();

    double FkM = 0.0;
    double FgM = 0.0;
    double FkV = 0.0;
    double FgV = 0.0;

    for (int j = 0; j < nsr; j++) {

      if (scheme[j] == SECTION_RESPONSE_MY) {
        FkM += Fs(j, j);

        for (int k = 0; k < nsr; k++) {
          if (scheme[k] == SECTION_RESPONSE_P)
            Fksb(i, 0) += Fs(j, k);
          if (scheme[k] == SECTION_RESPONSE_MY) {
            Fksb(i, 0) += wz(i) * Fs(j, k);
            Fksb(i, 3) += (xi[i] - 1) * Fs(j, k);
            Fksb(i, 4) += xi[i] * Fs(j, k);
          }
          if (scheme[k] == SECTION_RESPONSE_VZ) {
            FkV += Fs(j, k);

            Fksb(i, 0) -= wpz(i) * Fs(j, k);
            Fksb(i, 3) -= oneOverL * Fs(j, k);
            Fksb(i, 4) -= oneOverL * Fs(j, k);
          }
        }
      }
      if (scheme[j] == SECTION_RESPONSE_VZ) {
        isGamma = true;
        FgV += Fs(j, j);

        for (int k = 0; k < nsr; k++) {
          if (scheme[k] == SECTION_RESPONSE_P)
            Fgsb(i, 0) += Fs(j, k);
          if (scheme[k] == SECTION_RESPONSE_MY) {
            FgM += Fs(j, k);

            Fgsb(i, 0) += wz(i) * Fs(j, k);
            Fgsb(i, 3) += (xi[i] - 1) * Fs(j, k);
            Fgsb(i, 4) += xi[i] * Fs(j, k);
          }
          if (scheme[k] == SECTION_RESPONSE_VZ) {
            Fgsb(i, 0) -= wpz(i) * Fs(j, k);
            Fgsb(i, 3) -= oneOverL * Fs(j, k);
            Fgsb(i, 4) -= oneOverL * Fs(j, k);
          }
        }
      }
    }

    isGamma = shear_flag && isGamma;

    A(i, i)                             = 1.0;
    A(i + numSections, i + numSections) = 1.0;

    double q1 = q(0);

    for (int j = 0; j < numSections; j++) {
      A(j, i) -= q1 * L * L * FkM * lsk(j, i);
      if (isGamma) {
        A(j, i) -= q1 * L * FgM * lsg(j, i);

        A(j, i + numSections) += q1 * L * L * FkV * lsk(j, i);
        A(j, i + numSections) += q1 * L * FgV * lsg(j, i);

        A(j + numSections, i) -= q1 * L * FkM * lskp(j, i);
        A(j + numSections, i) -= q1 * FgM * lsgp(j, i);

        A(j + numSections, i + numSections) += q1 * L * FkV * lskp(j, i);
        A(j + numSections, i + numSections) += q1 * FgV * lsgp(j, i);
      }
    }
  }

  Matrix mhs(numSections, nq);

  mhs.addMatrixProduct(0.0, lsk, Fksb, L * L);
  if (isGamma)
    mhs.addMatrixProduct(1.0, lsg, Fgsb, L);

  for (int i = 0; i < numSections; i++)
    for (int j = 0; j < nq; j++)
      b(i, j) = mhs(i, j);

  if (isGamma) {
    mhs.addMatrixProduct(0.0, lskp, Fksb, L);
    mhs.addMatrixProduct(1.0, lsgp, Fgsb, 1.0);
    for (int i = 0; i < numSections; i++)
      for (int j = 0; j < nq; j++)
        b(i + numSections, j) = mhs(i, j);
  }

  A.Solve(b, dwzidq);

  return;
}


void
ForceDeltaFrame3d::computeSectionForces(VectorND<nsr>& sp, int isec)
{

  int numSections = points.size();
  double L = theCoordTransf->getInitialLength();

//double xi[maxNumSections];
//stencil->getSectionLocations(numSections, L, xi);
  double x = xi[isec] * L;


  for (auto[load, loadFactor] : eleLoads) {

    int type;
    const Vector& data = load->getData(type, loadFactor);

    if (type == LOAD_TAG_Beam3dUniformLoad) {
      double wy = data(0) * loadFactor; // Transverse
      double wz = data(1) * loadFactor; // Transverse
      double wa = data(2) * loadFactor; // Axial

      for (int ii = 0; ii < nsr; ii++) {

        switch (scheme[ii]) {
        case SECTION_RESPONSE_P:  sp[ii] += wa * (L - x); break;
        case SECTION_RESPONSE_MZ: sp[ii] += wy * 0.5 * x * (x - L); break;
        case SECTION_RESPONSE_VY: sp[ii] += wy * (x - 0.5 * L); break;
        case SECTION_RESPONSE_MY: sp[ii] += wz * 0.5 * x * (L - x); break;
        case SECTION_RESPONSE_VZ: sp[ii] += wz * (0.5 * L - x); break;
        default:                  break;
        }
      }
    } 
    else if (type == LOAD_TAG_Beam3dPartialUniformLoad) {
      double wy = data(0) * loadFactor;  // Transverse Y at start
      double wz = data(1) * loadFactor;  // Transverse Z at start
      double wa = data(2) * loadFactor;  // Axial at start
      double a = data(3)*L;
      double b = data(4)*L;
      double wyb = data(5) * loadFactor;  // Transverse Y at end
      double wzb = data(6) * loadFactor;  // Transverse Z at end
      double wab = data(7) * loadFactor;  // Axial at end
      double Fa = wa * (b - a) + 0.5 * (wab - wa) * (b - a); // resultant axial load
      double Fy = wy * (b - a); // resultant transverse load
      double Fz = wz * (b - a); // resultant transverse load
      double c = a + 0.5 * (b - a);
      double VyI = Fy * (1 - c / L);
      double VyJ = Fy * c / L;
      double VzI = Fz * (1 - c / L);
      double VzJ = Fz * c / L;
      Fy = 0.5 * (wyb - wy) * (b - a); // resultant transverse load
      Fz = 0.5 * (wzb - wz) * (b - a); // resultant transverse load
      c = a + 2.0 / 3.0 * (b - a);
      VyI += Fy * (1 - c / L);
      VyJ += Fy * c / L;
      VzI += Fz * (1 - c / L);
      VzJ += Fz * c / L;
     
      for (int ii = 0; ii < nsr; ii++) {
        if (x <= a) {
          switch(scheme[ii]) {
          case SECTION_RESPONSE_P:
            sp(ii) += Fa;
            break;
          case SECTION_RESPONSE_MZ:
            sp(ii) -= VyI*x;
            break;
          case SECTION_RESPONSE_MY:
            sp(ii) += VzI*x;
            break;            
          case SECTION_RESPONSE_VY:
            sp(ii) -= VyI;
            break;
          case SECTION_RESPONSE_VZ:
        sp(ii) += VzI;
            break;            
          default:
            break;
          }
        }
        else if (x >= b) {
          switch(scheme[ii]) {
          case SECTION_RESPONSE_MZ:
            sp(ii) += VyJ*(x-L);
            break;
          case SECTION_RESPONSE_MY:
            sp(ii) -= VzJ*(x-L);
            break;            
          case SECTION_RESPONSE_VY:
            sp(ii) += VyJ;
            break;
          case SECTION_RESPONSE_VZ:
            sp(ii) -= VzJ;            
            break;
          default:
            break;
          }
        }
        else {
          double wyy = wy + (wyb - wy) / (b - a) * (x - a);
          double wzz = wz + (wzb - wz) / (b - a) * (x - a);
          switch(scheme[ii]) {
          case SECTION_RESPONSE_P:
            sp(ii) += Fa - wa * (x - a) - 0.5 * (wab - wa) / (b - a) * (x - a) * (x - a);
            break;
          case SECTION_RESPONSE_MZ:
            sp(ii) += -VyI * x + 0.5 * wy * (x - a) * (x - a) + 0.5 * (wyy - wy) * (x - a) * (x - a) / 3.0;
            break;
          case SECTION_RESPONSE_MY:
            sp(ii) += VzI * x - 0.5 * wz * (x - a) * (x - a) - 0.5 * (wzz - wz) * (x - a) * (x - a) / 3.0;
            break;            
          case SECTION_RESPONSE_VY:
            sp(ii) += -VyI + wy * (x - a) + 0.5 * (wyy - wy) * (x - a);
            break;
          case SECTION_RESPONSE_VZ:           
            sp(ii) -= -VzI + wz * (x - a) - 0.5 * (wzz - wz) * (x - a);
            break;
          default:
            break;
          }
        }
      }
    }
    else if (type == LOAD_TAG_Beam3dPointLoad) {
      double Py     = data(0) * loadFactor;
      double Pz     = data(1) * loadFactor;
      double N      = data(2) * loadFactor;
      double aOverL = data(3);

      if (aOverL < 0.0 || aOverL > 1.0)
        continue;

      double a = aOverL * L;

      double Vy1 = Py * (1.0 - aOverL);
      double Vy2 = Py * aOverL;

      double Vz1 = Pz * (1.0 - aOverL);
      double Vz2 = Pz * aOverL;

      for (int ii = 0; ii < nsr; ii++) {

        if (x <= a) {
          switch (scheme[ii]) {
          case SECTION_RESPONSE_P:  sp[ii] += N; break;
          case SECTION_RESPONSE_MZ: sp[ii] -= x * Vy1; break;
          case SECTION_RESPONSE_VY: sp[ii] -= Vy1; break;
          case SECTION_RESPONSE_MY: sp[ii] += x * Vz1; break;
          case SECTION_RESPONSE_VZ: sp[ii] -= Vz1; break;
          default:                  break;
          }
        } else {
          switch (scheme[ii]) {
          case SECTION_RESPONSE_MZ: sp[ii] -= (L - x) * Vy2; break;
          case SECTION_RESPONSE_VY: sp[ii] += Vy2; break;
          case SECTION_RESPONSE_MY: sp[ii] += (L - x) * Vz2; break;
          case SECTION_RESPONSE_VZ: sp[ii] += Vz2; break;
          default:                  break;
          }
        }
      }
    } else {
      opserr << "ForceDeltaFrame3d::addLoad -- load type unknown for element with tag: "
             << this->getTag() << "\n";
    }
  }
}

void
ForceDeltaFrame3d::getStressGrad(VectorND<nsr>& dspdh, int isec, int igrad)
{
  int numSections = points.size();

  double L    = theCoordTransf->getInitialLength();
  double dLdh = theCoordTransf->getLengthGrad();

  double xi[maxNumSections];
  stencil->getSectionLocations(numSections, L, xi);

  double dxidh[maxNumSections];
  stencil->getLocationsDeriv(numSections, L, dLdh, dxidh);

  double x    = xi[isec] * L;
  double dxdh = xi[isec] * dLdh + dxidh[isec] * L;

  int order      = points[isec].material->getOrder();
  const ID& code = points[isec].material->getType();

  for (auto[load, loadFactor] : eleLoads) {
    int type;
    const  Vector& data = load->getData(type, loadFactor);


    if (type == LOAD_TAG_Beam3dUniformLoad) {
      double wy = data(0) * 1.0; // Transverse
      double wz = data(1) * 1.0; // Transverse
      double wa = data(2) * 1.0; // Axial

      const Vector& sens = load->getSensitivityData(igrad);
      double dwydh       = sens(0);
      double dwzdh       = sens(1);
      double dwadh       = sens(2);
      for (int ii = 0; ii < nsr; ii++) {

        switch (code(ii)) {
        case SECTION_RESPONSE_P:
          //sp[ii] += wa*(L-x);
          dspdh(ii) += dwadh * (L - x) + wa * (dLdh - dxdh);
          break;
        case SECTION_RESPONSE_MZ:
          //sp[ii] += wy*0.5*x*(x-L);
          //dspdh(ii) += 0.5 * (dwydh*x*(x-L) + wy*dxdh*(x-L) + wy*x*(dxdh-dLdh));
          dspdh(ii) += 0.5 * (dwydh * x * (x - L) + wy * (dxdh * (2 * x - L) - x * dLdh));
          break;
        case SECTION_RESPONSE_VY:
          //sp[ii] += wy*(x-0.5*L);
          dspdh(ii) += dwydh * (x - 0.5 * L) + wy * (dxdh - 0.5 * dLdh);
          break;
        case SECTION_RESPONSE_MY:
          //sp[ii] += wz*0.5*x*(L-x);
          //dspdh(ii) += 0.5*(dwzdh*x*(L-x) + wz*dxdh*(L-x) + wz*x*(dLdh-dxdh));
          dspdh(ii) += 0.5 * (dwzdh * x * (L - x) + wz * (dxdh * (L - 2 * x) + x * dLdh));
          break;
        case SECTION_RESPONSE_VZ:
          //sp[ii] += wz*(x-0.5*L);
          dspdh(ii) += dwzdh * (0.5 * L - x) + wz * (0.5 * dLdh - dxdh);
          break;
        default: break;
        }
      }

    } else if (type == LOAD_TAG_Beam3dPointLoad) {
      double Py     = data(0) * 1.0;
      double Pz     = data(1) * 1.0;
      double N      = data(2) * 1.0;
      double aOverL = data(3);

      if (aOverL < 0.0 || aOverL > 1.0)
        continue;

      const Vector& sens = load->getSensitivityData(igrad);
      double dPydh       = sens(0);
      double dPzdh       = sens(1);
      double dNdh        = sens(2);
      double daLdh       = sens(3);

      double a = aOverL * L;

      double Vy1    = Py * (1.0 - aOverL);
      double Vy2    = Py * aOverL;
      double dVy1dh = Py * (0.0 - daLdh) + dPydh * (1.0 - aOverL);
      double dVy2dh = Py * daLdh + dPydh * aOverL;

      double Vz1    = Pz * (1.0 - aOverL);
      double Vz2    = Pz * aOverL;
      double dVz1dh = Pz * (0.0 - daLdh) + dPzdh * (1.0 - aOverL);
      double dVz2dh = Pz * daLdh + dPzdh * aOverL;

      for (int ii = 0; ii < nsr; ii++) {

        if (x <= a) {
          switch (code(ii)) {
          case SECTION_RESPONSE_P:
            //sp[ii] += N;
            dspdh(ii) += dNdh;
            break;
          case SECTION_RESPONSE_MZ:
            //sp[ii] -= x*Vy1;
            dspdh(ii) -= (dxdh * Vy1 + x * dVy1dh);
            break;
          case SECTION_RESPONSE_VY:
            //sp[ii] -= Vy1;
            dspdh(ii) -= dVy1dh;
            break;
          case SECTION_RESPONSE_MY:
            //sp[ii] += x*Vz1;
            dspdh(ii) += (dxdh * Vz1 + x * dVz1dh);
            break;
          case SECTION_RESPONSE_VZ:
            //sp[ii] -= Vz1;
            dspdh(ii) -= dVz1dh;
            break;

          default: break;
          }
        } else {
          switch (code(ii)) {
          case SECTION_RESPONSE_MZ:
            //sp[ii] -= (L-x)*Vy2;
            dspdh(ii) -= (dLdh - dxdh) * Vy2 + (L - x) * dVy2dh;
            break;
          case SECTION_RESPONSE_VY:
            //sp[ii] += Vy2;
            dspdh(ii) += dVy2dh;
            break;
          case SECTION_RESPONSE_MY:
            //sp[ii] += (L-x)*Vz2;
            dspdh(ii) += (dLdh - dxdh) * Vz2 + (L - x) * dVz2dh;
            break;
          case SECTION_RESPONSE_VZ:
            //sp[ii] += Vz2;
            dspdh(ii) += dVz2dh;
            break;
          default: break;
          }
        }
      }
    } else {
      opserr << "ForceDeltaFrame3d::getStressGrad -- load type unknown for element "
                "with tag: "
             << this->getTag() << "\n";
    }
  }
}

VectorND<6>&
ForceDeltaFrame3d::getBasicForce()
{
  return q_pres;
}

MatrixND<6, 6>&
ForceDeltaFrame3d::getBasicTangent(State state, int rate)
{
  return K_pres;
}


int
ForceDeltaFrame3d::getInitialFlexibility(Matrix& fe)
{
  int numSections = points.size();
  fe.Zero();

  double L        = theCoordTransf->getInitialLength();
  double oneOverL = 1.0 / L;

  double xi[maxNumSections];
  stencil->getSectionLocations(numSections, L, xi);

  double wt[maxNumSections];
  stencil->getSectionWeights(numSections, L, wt);

  for (int i = 0; i < numSections; i++) {

    int order      = points[i].material->getOrder();
    const ID& code = points[i].material->getType();

    MatrixND<nsr, nq> fb;

    double xL  = xi[i];
    double xL1 = xL - 1.0;
    double wtL = wt[i] * L;

    const Matrix& fSec = points[i].material->getInitialFlexibility();
    fb.zero();
    double tmp;
    int ii, jj;
    for (int ii = 0; ii < nsr; ii++) {
      switch (code(ii)) {
      case SECTION_RESPONSE_P:
        for (int jj = 0; jj < nsr; jj++)
          fb(jj, 0) += fSec(jj, ii) * wtL;
        break;
      case SECTION_RESPONSE_MZ:
        for (int jj = 0; jj < nsr; jj++) {
          tmp = fSec(jj, ii) * wtL;
          fb(jj, 1) += xL1 * tmp;
          fb(jj, 2) += xL * tmp;
        }
        break;
      case SECTION_RESPONSE_VY:
        for (int jj = 0; jj < nsr; jj++) {
          tmp = oneOverL * fSec(jj, ii) * wtL;
          fb(jj, 1) += tmp;
          fb(jj, 2) += tmp;
        }
        break;
      case SECTION_RESPONSE_MY:
        for (int jj = 0; jj < nsr; jj++) {
          tmp = fSec(jj, ii) * wtL;
          fb(jj, 3) += xL1 * tmp;
          fb(jj, 4) += xL * tmp;
        }
        break;
      case SECTION_RESPONSE_VZ:
        for (int jj = 0; jj < nsr; jj++) {
          tmp = oneOverL * fSec(jj, ii) * wtL;
          fb(jj, 3) += tmp;
          fb(jj, 4) += tmp;
        }
        break;
      case SECTION_RESPONSE_T:
        for (int jj = 0; jj < nsr; jj++)
          fb(jj, 5) += fSec(jj, ii) * wtL;
        break;
      default: break;
      }
    }
    for (int ii = 0; ii < nsr; ii++) {
      switch (code(ii)) {
      case SECTION_RESPONSE_P:
        for (int jj = 0; jj < nq; jj++)
          fe(0, jj) += fb(ii, jj);
        break;
      case SECTION_RESPONSE_MZ:
        for (int jj = 0; jj < nq; jj++) {
          tmp = fb(ii, jj);
          fe(1, jj) += xL1 * tmp;
          fe(2, jj) += xL * tmp;
        }
        break;
      case SECTION_RESPONSE_VY:
        for (int jj = 0; jj < nq; jj++) {
          tmp = oneOverL * fb(ii, jj);
          fe(1, jj) += tmp;
          fe(2, jj) += tmp;
        }
        break;
      case SECTION_RESPONSE_MY:
        for (int jj = 0; jj < nq; jj++) {
          tmp = fb(ii, jj);
          fe(3, jj) += xL1 * tmp;
          fe(4, jj) += xL * tmp;
        }
        break;
      case SECTION_RESPONSE_VZ:
        for (int jj = 0; jj < nq; jj++) {
          tmp = oneOverL * fb(ii, jj);
          fe(3, jj) += tmp;
          fe(4, jj) += tmp;
        }
        break;
      case SECTION_RESPONSE_T:
        for (int jj = 0; jj < nq; jj++)
          fe(5, jj) += fb(ii, jj);
        break;
      default: break;
      }
    }
  }

  return 0;
}

int
ForceDeltaFrame3d::getInitialDeformations(Vector& v0)
{
  int numSections = points.size();

  v0.Zero();
  if (eleLoads.size() < 1)
    return 0;

  double L        = theCoordTransf->getInitialLength();
  double oneOverL = 1.0 / L;

  double xi[maxNumSections];
  stencil->getSectionLocations(numSections, L, xi);

  double wt[maxNumSections];
  stencil->getSectionWeights(numSections, L, wt);

  for (int i = 0; i < numSections; i++) {

    double xL  = xi[i];
    double xL1 = xL - 1.0;
    double wtL = wt[i] * L;

    VectorND<nsr> sp;
    sp.zero();

    this->computeSectionForces(sp, i);

    MatrixND<nsr,nsr> fse = points[i].material->getFlexibility<nsr,scheme>(State::Init);

    VectorND<nsr> e;
    e.addMatrixVector(0.0, fse, sp, 1.0);

    double tmp;
    for (int ii = 0; ii < nsr; ii++) {
      double dei = e[ii] * wtL;
      switch (scheme[ii]) {
      case SECTION_RESPONSE_P: 
        v0(0) += dei; break;
      case SECTION_RESPONSE_MZ:
        v0(1) += xL1 * dei;
        v0(2) += xL * dei;
        break;
      case SECTION_RESPONSE_VY:
        tmp = oneOverL * dei;
        v0(1) += tmp;
        v0(2) += tmp;
        break;
      case SECTION_RESPONSE_MY:
        v0(3) += xL1 * dei;
        v0(4) += xL * dei;
        break;
      case SECTION_RESPONSE_VZ:
        tmp = oneOverL * dei;
        v0(3) += tmp;
        v0(4) += tmp;
        break;
      case SECTION_RESPONSE_T: v0(5) += dei; break;
      default:                 break;
      }
    }
  }

  return 0;
}



void
ForceDeltaFrame3d::computedwdh(double dwidh[], int igrad, const Vector& q)
{
  int numSections = points.size();

  double L        = theCoordTransf->getInitialLength();
  double oneOverL = 1.0 / L;

  double xi[maxNumSections];
  stencil->getSectionLocations(numSections, L, xi);

  Matrix G(numSections, numSections);
  vandermonde(numSections, xi, G);

  Matrix Ginv(numSections, numSections);
  vandermonde_inverse(numSections, xi, Ginv);

  Matrix Hk(numSections, numSections);
  this->getHk(numSections, xi, Hk);

  Matrix ls(numSections, numSections);
  ls.addMatrixProduct(0.0, Hk, Ginv, 1.0);

  Matrix Hg(numSections, numSections);
  this->getHg(numSections, xi, Hg);

  Matrix lsg(numSections, numSections);
  lsg.addMatrixProduct(0.0, Hg, Ginv, 1.0);

  Matrix Hkp(numSections, numSections);
  this->getHkp(numSections, xi, Hkp);

  Matrix lskp(numSections, numSections);
  lskp.addMatrixProduct(0.0, Hkp, Ginv, 1.0);

  Matrix Hgp(numSections, numSections);
  this->getHgp(numSections, xi, Hgp);

  Matrix lsgp(numSections, numSections);
  lsgp.addMatrixProduct(0.0, Hgp, Ginv, 1.0);

  double dLdh = theCoordTransf->getLengthGrad();
  double dxidh[maxNumSections];
  stencil->getLocationsDeriv(numSections, L, dLdh, dxidh);

  bool isdxidh = false;
  for (int i = 0; i < numSections; i++) {
    dxidh[i] = dxidh[i]; // - xi[i]/L*dLdh;
    if (dxidh[i] != 0.0)
      isdxidh = true;
  }

  Matrix A(2 * numSections, 2 * numSections);
  Vector b(2 * numSections);

  Vector Fksdsdh(numSections);
  Vector Fgsdsdh(numSections);

  Vector kappa(numSections);
  Vector gamma(numSections);

  const double q1   = q(0);
  double q2q3 = q(1) + q(2);


  for (int i = 0; i < numSections; i++) {

    const Matrix& fs   = points[i].material->getSectionFlexibility();
    const Vector& dsdh = points[i].material->getStressResultantSensitivity(igrad, true);
    Fksdsdh(i)         = 0.0;
    Fgsdsdh(i)         = 0.0;

    double FkM = 0.0;
    double FgM = 0.0;
    double FkV = 0.0;
    double FgV = 0.0;

    const ID& code = points[i].material->getType();
    int order      = points[i].material->getOrder();
    for (int j = 0; j < nsr; j++) {
      if (scheme[j] == SECTION_RESPONSE_MZ) {
        FkM += fs(j, j);
        kappa(i) += (points[i].es)(j);
        for (int k = 0; k < nsr; k++) {
          Fksdsdh(i) -= fs(j, k) * dsdh(k);
          if (scheme[k] == SECTION_RESPONSE_VY)
            FkV += fs(j, k);
        }
      }
      if (scheme[j] == SECTION_RESPONSE_VY) {
        FgV += fs(j, j);
        gamma(i) += (points[i].es)(j);
        for (int k = 0; k < nsr; k++) {
          Fgsdsdh(i) -= fs(j, k) * dsdh(k);
          if (scheme[k] == SECTION_RESPONSE_MZ)
            FgM += fs(j, k);
        }
      }
    }


    Fksdsdh(i) += q2q3 * FkM * dxidh[i];

    if (shear_flag) {
      Fksdsdh(i) += q2q3 * oneOverL * oneOverL * FkV * dLdh;
      Fgsdsdh(i) += q2q3 * FgM * dxidh[i];
      Fgsdsdh(i) += q2q3 * oneOverL * oneOverL * FgV * dLdh;
    }

    A(i, i)                             = 1.0;
    A(i + numSections, i + numSections) = 1.0;

    for (int j = 0; j < numSections; j++) {
      A(j, i) -= q1 * L * L * FkM * ls(j, i);
      if (shear_flag) {
        A(j, i) -= q1 * L * FgM * lsg(j, i);

        A(j, i + numSections) += q1 * L * L * FkV * ls(j, i);
        A(j, i + numSections) += q1 * L * FgV * lsg(j, i);

        A(j + numSections, i) -= q1 * L * FkM * lskp(j, i);
        A(j + numSections, i) -= q1 * FgM * lsgp(j, i);

        A(j + numSections, i + numSections) += q1 * L * FkV * lskp(j, i);
        A(j + numSections, i + numSections) += q1 * FgV * lsgp(j, i);
      }
    }
  }

  Vector mhs(numSections);

  mhs.addMatrixVector(0.0, ls, Fksdsdh, L * L);
  mhs.addMatrixVector(1.0, ls, kappa, 2 * L * dLdh);
  if (shear_flag) {
    mhs.addMatrixVector(1.0, lsg, Fgsdsdh, L);
    mhs.addMatrixVector(1.0, lsg, gamma, dLdh);
  }
  for (int i = 0; i < numSections; i++)
    b(i) = mhs(i);

  if (shear_flag) {
    mhs.addMatrixVector(0.0, lskp, Fksdsdh, L);
    mhs.addMatrixVector(1.0, lsgp, Fgsdsdh, 1.0);
    mhs.addMatrixVector(1.0, lskp, kappa, dLdh);
    //mhs.addMatrixVector(1.0, lsgp, gamma, 0*dLdh);
    for (int i = 0; i < numSections; i++)
      b(i + numSections) = mhs(i);
  }


  if (isdxidh) {
    Matrix dGdh(numSections, numSections);
    for (int i = 0; i < numSections; i++) {
      dGdh(i, 0) = 0;
      for (int j = 1; j < numSections; j++) {
        dGdh(i, j) = j * pow(xi[i], j - 1) * dxidh[i];
      }
    }

    Matrix dlsdh(numSections, numSections);


    Matrix dHkdh(numSections, numSections);
    for (int i = 0; i < numSections; i++) {
      for (int j = 0; j < numSections; j++) {
        dHkdh(i, j) = (pow(xi[i], j + 1) / (j + 1) - 1.0 / (j + 1) / (j + 2)) * dxidh[i];
      }
    }
    dlsdh.addMatrixProduct(0.0, dHkdh, Ginv, 1.0);
    dlsdh.addMatrixProduct(1.0, ls * dGdh, Ginv, -1.0);
    mhs.addMatrixVector(0.0, dlsdh, kappa, L * L);

    if (shear_flag) {
      Matrix dHgdh(numSections, numSections);
      for (int i = 0; i < numSections; i++) {
        for (int j = 0; j < numSections; j++) {
          dHgdh(i, j) = (pow(xi[i], j) - 1.0 / (j + 1)) * dxidh[i];
        }
      }
      dlsdh.addMatrixProduct(0.0, dHgdh, Ginv, 1.0);
      dlsdh.addMatrixProduct(1.0, lsg * dGdh, Ginv, -1.0);
      mhs.addMatrixVector(1.0, dlsdh, gamma, L);
    }

    for (int i = 0; i < numSections; i++)
      b[i] += mhs[i];


    if (shear_flag) {
      Matrix dHkpdh(numSections, numSections);
      for (int i = 0; i < numSections; i++) {
        for (int j = 0; j < numSections; j++) {
          dHkpdh(i, j) = pow(xi[i], j) * dxidh[i];
        }
      }
      dlsdh.addMatrixProduct(0.0, dHkpdh, Ginv, 1.0);
      dlsdh.addMatrixProduct(1.0, lskp * dGdh, Ginv, -1.0);
      mhs.addMatrixVector(0.0, dlsdh, kappa, L);

      Matrix dHgpdh(numSections, numSections);
      for (int i = 0; i < numSections; i++) {
        dHgpdh(i, 0) = 0.0;
        for (int j = 1; j < numSections; j++) {
          dHgpdh(i, j) = (j * pow(xi[i], j - 1)) * dxidh[i];
        }
      }
      dlsdh.addMatrixProduct(0.0, dHgpdh, Ginv, 1.0);
      dlsdh.addMatrixProduct(1.0, lsgp * dGdh, Ginv, -1.0);
      mhs.addMatrixVector(1.0, dlsdh, gamma, 1.0);

      for (int i = 0; i < numSections; i++)
        b(i + numSections) += mhs(i);
    }
  }


  Vector ajs(dwidh, 2 * numSections);

  A.Solve(b, ajs);

  return;
}


void
ForceDeltaFrame3d::compSectionDisplacements(Vector sectionCoords[], Vector sectionDispls[]) const
{
  int numSections = points.size();
  // get basic displacements and increments
  static Vector ub(nq);
  ub = theCoordTransf->getBasicTrialDisp();

  double L = theCoordTransf->getInitialLength();

  // get integration point positions and weights
  static double xi_pts[maxNumSections];
  stencil->getSectionLocations(numSections, L, xi_pts);

  //
  // setup Vandermode and CBDI influence matrices
  //

  // get CBDI influence matrix
  Matrix ls(numSections, numSections);
  getCBDIinfluenceMatrix(numSections, xi_pts, L, ls);

  // get section curvatures
  Vector kappa(numSections); // curvature
  static Vector vs;          // section deformations

  for (int i = 0; i < numSections; i++) {
    // THIS IS VERY INEFFICIENT ... CAN CHANGE LATER
    int sectionKey = 0;
    const ID& code = points[i].material->getType();
    int ii;
    for (ii = 0; ii < code.Size(); ii++)
      if (code(ii) == SECTION_RESPONSE_MZ) {
        sectionKey = ii;
        break;
      }

    if (ii == code.Size()) {
      opserr
          << "FATAL NLBeamColumnCBDI3d::compSectionDispls - section does not provide Mz response\n";
    }

    // get section deformations
    vs       = points[i].material->getSectionDeformation();
    kappa(i) = vs(sectionKey);
  }

  Vector w(numSections);
  VectorND<ndm> xl, uxb;
  VectorND<ndm> xg, uxg;

  // w = ls * kappa;
  w.addMatrixVector(0.0, ls, kappa, 1.0);

  for (int i = 0; i < numSections; i++) {
    double xi = xi_pts[i];

    xl(0) = xi * L;
    xl(1) = 0;

    // get section global coordinates
    sectionCoords[i] = theCoordTransf->getPointGlobalCoordFromLocal(xl);

    // compute section displacements
    uxb(0) = xi * ub(0); // consider linear variation for axial displacement. CHANGE LATER!!!!!!!!!!
    uxb(1) = w(i);

    // get section displacements in global system
    sectionDispls[i] = theCoordTransf->getPointGlobalDisplFromBasic(xi, uxb);
  }
  return;
}




void
ForceDeltaFrame3d::Print(OPS_Stream& s, int flag)
{
  const int numSections = points.size();
  const ID& node_tags = this->getExternalNodes();

  if (flag == OPS_PRINT_PRINTMODEL_JSON) {
    s << OPS_PRINT_JSON_ELEM_INDENT << "{";
    s << "\"name\": " << this->getTag() << ", ";
    s << "\"type\": \"" << this->getClassType() << "\"";
    s << ", ";

    s << "\"nodes\": [" << node_tags(0) << ", " 
                        << node_tags(1) << "]";
    s << ", ";

    s << "\"massperlength\": " << density ;
    s << ", ";

    s << "\"sections\": [";
    for (int i = 0; i < numSections - 1; i++)
      s << points[i].material->getTag() << ", ";
    s << points[numSections - 1].material->getTag() << "]";
    s << ", ";

    s << "\"crdTransformation\": " << theCoordTransf->getTag();
    s << ", ";

    s << "\"integration\": ";
    stencil->Print(s, flag);
    s << "}";

    return;
  }

  if (flag == 2) {

    s << "#ForceDeltaFrame2D\n";

    const Vector& xi  = theNodes[0]->getCrds();
    const Vector& xj  = theNodes[1]->getCrds();
    const Vector& ui = theNodes[0]->getDisp();
    const Vector& uj = theNodes[1]->getDisp();

    s << "#NODE " << xi(0) << " " << xi(1) << " " << ui(0) << " " << ui(1)
      << " " << ui(2) << "\n";

    s << "#NODE " << xj(0) << " " << xj(1) << " " << uj(0) << " " << uj(1)
      << " " << uj(2) << "\n";
  }

  if (flag == OPS_PRINT_CURRENTSTATE) {

    s << "\nEment: " << this->getTag() << " Type: ForceDeltaFrame3d ";
    s << "\tConnected Nodes: " << connectedExternalNodes;
    s << "\tNumber of Sections: " << numSections;
    s << "\tMass density: " << density << "\n";
    stencil->Print(s, flag);
    double P     = q_past(0);
    double M1    = q_past(1);
    double M2    = q_past(2);
    double L     = theCoordTransf->getInitialLength();
    double V     = (M1 + M2) / L;

    double p0[6];
    p0[0] = 0.0;
    p0[1] = 0.0;
    p0[2] = 0.0;
    p0[3] = 0.0;
    p0[4] = 0.0;
    p0[5] = 0.0;
    if (eleLoads.size() > 0)
      this->computeReactions(p0);

    s << "\tEnd 1 Forces (P V M): " << -P + p0[0] << " " << V + p0[1] << " " << M1 << "\n";
    s << "\tEnd 2 Forces (P V M): " << P << " " << -V + p0[2] << " " << M2 << "\n";

    if (flag == 1) {
      for (int i = 0; i < numSections; i++)
        s << "\nSection " << i << " :" << *points[i].material;
    }
  }

}


void
ForceDeltaFrame3d::setSectionPointers(int numSec, FrameSection** secPtrs)
{
  // Return value of 0 indicates success

  points.clear();

  for (int i = 0; i < numSec; i++) {
    FrameSection* section = secPtrs[i];

    assert(section != nullptr);

    points.push_back({
        .point=0,
        .weight=0,
        .material=section->getFrameCopy(scheme)
    });

  }
}


Response*
ForceDeltaFrame3d::setResponse(const char** argv, int argc, OPS_Stream& output)
{
  int numSections = points.size();
  Response* theResponse = nullptr;

  output.tag("ElementOutput");
  output.attr("eleType", "ForceDeltaFrame3d");
  output.attr("eleTag", this->getTag());
  output.attr("node1", connectedExternalNodes[0]);
  output.attr("node2", connectedExternalNodes[1]);

  // Global force
  if (strcmp(argv[0],"forces") == 0 || 
      strcmp(argv[0],"force") == 0  ||
      strcmp(argv[0],"globalForce") == 0 ||
      strcmp(argv[0],"globalForces") == 0) {

    output.tag("ResponseType", "Px_1");
    output.tag("ResponseType", "Py_1");
    output.tag("ResponseType", "Mz_1");
    output.tag("ResponseType", "Px_2");
    output.tag("ResponseType", "Py_2");
    output.tag("ResponseType", "Mz_2");

    theResponse = new ElementResponse(this, 1, Vector(12));


  // Local force
  }  else if (strcmp(argv[0],"localForce") == 0 || 
              strcmp(argv[0],"localForces") == 0) {

    output.tag("ResponseType", "N_1");
    output.tag("ResponseType", "Vy_1");
    output.tag("ResponseType", "Vz_1");
    output.tag("ResponseType", "T_1");
    output.tag("ResponseType", "My_1");
    output.tag("ResponseType", "Mz_1");
    output.tag("ResponseType", "N_2");
    output.tag("ResponseType", "Vy_2");
    output.tag("ResponseType", "Vz_2");
    output.tag("ResponseType", "T_2");
    output.tag("ResponseType", "My_2");
    output.tag("ResponseType", "Mz_2");

    theResponse = new ElementResponse(this, 2, Vector(12));


    // basic force -
  } else if (strcmp(argv[0], "basicForce") == 0 || strcmp(argv[0], "basicForces") == 0) {

    output.tag("ResponseType", "N");
    output.tag("ResponseType", "M_1");
    output.tag("ResponseType", "M_2");

    theResponse = new ElementResponse(this, 7, Vector(6));

  // chord rotation -
  } else if (strcmp(argv[0], "chordRotation") == 0 || strcmp(argv[0], "chordDeformation") == 0 ||
             strcmp(argv[0], "basicDeformation") == 0) {

    output.tag("ResponseType", "eps");
    output.tag("ResponseType", "theta_1");
    output.tag("ResponseType", "theta_2");

    theResponse = new ElementResponse(this, 3, Vector(6));

  // plastic rotation -
  } else if (strcmp(argv[0], "plasticRotation") == 0 ||
             strcmp(argv[0], "plasticDeformation") == 0) {

    output.tag("ResponseType", "epsP");
    output.tag("ResponseType", "thetaP_1");
    output.tag("ResponseType", "thetaP_2");

    theResponse = new ElementResponse(this, 4, Vector(6));

  // point of inflection
  } else if (strcmp(argv[0], "inflectionPoint") == 0) {

    output.tag("ResponseType", "inflectionPoint");

    theResponse = new ElementResponse(this, 5, 0.0);

    // tangent drift
  } else if (strcmp(argv[0], "tangentDrift") == 0) {
    theResponse = new ElementResponse(this, 6, Vector(4));

    // basic forces
  } else if (strcmp(argv[0], "basicForce") == 0)
    theResponse = new ElementResponse(this, 7, q_pres);

  /*
  // Curvature sensitivity
  else if (strcmp(argv[0],"dcurvdh") == 0)
    return new ElementResponse(this, 7, Vector(numSections));

  // basic deformation sensitivity
  else if (strcmp(argv[0],"dvdh") == 0)
    return new ElementResponse(this, 8, Vector(3));
  */

  // plastic deformation sensitivity
  else if (strcmp(argv[0], "dvpdh") == 0)
    return new ElementResponse(this, 9, Vector(6));

  // basic force sensitivity
  else if (strcmp(argv[0], "dqdh") == 0)
    return new ElementResponse(this, 12, Vector(6));

  else if (strcmp(argv[0], "integrationPoints") == 0)
    theResponse = new ElementResponse(this, 10, Vector(numSections));

  else if (strcmp(argv[0], "integrationWeights") == 0)
    theResponse = new ElementResponse(this, 11, Vector(numSections));

  else if (strcmp(argv[0], "sectionTags") == 0)
    theResponse = new ElementResponse(this, 110, ID(numSections));

  else if (strcmp(argv[0], "sectionDisplacements") == 0)
    theResponse = new ElementResponse(this, 111, Matrix(numSections, 3));

  else if (strcmp(argv[0], "cbdiDisplacements") == 0)
    theResponse = new ElementResponse(this, 112, Matrix(20, 3));

  // section response -
  else if (strstr(argv[0], "sectionX") != 0) {
    if (argc > 2) {
      float sectionLoc = atof(argv[1]);

      double xi[maxNumSections];
      double L = theCoordTransf->getInitialLength();
      stencil->getSectionLocations(numSections, L, xi);

      sectionLoc /= L;

      float minDistance = fabs(xi[0] - sectionLoc);
      int sectionNum    = 0;
      for (int i = 1; i < numSections; i++) {
        if (fabs(xi[i] - sectionLoc) < minDistance) {
          minDistance = fabs(xi[i] - sectionLoc);
          sectionNum  = i;
        }
      }

      output.tag("GaussPointOutput");
      output.attr("number", sectionNum + 1);
      output.attr("eta", xi[sectionNum] * L);

      if (strcmp(argv[2], "dsdh") != 0) {
        theResponse = points[sectionNum].material->setResponse(&argv[2], argc - 2, output);
      } else {
        int order         = points[sectionNum].material->getOrder();
        theResponse       = new ElementResponse(this, 76, Vector(order));
        Information& info = theResponse->getInformation();
        info.theInt       = sectionNum;
      }
    }
  }

  // section response -
  else if (strstr(argv[0], "section") != 0) {

    if (argc > 1) {

      int sectionNum = atoi(argv[1]);

      double xi[maxNumSections];

      if (sectionNum > 0 && sectionNum <= numSections && argc > 2) {
        FrameSection* section = points[sectionNum - 1].material;
        double L = theCoordTransf->getInitialLength();
        stencil->getSectionLocations(numSections, L, xi);

        output.tag("GaussPointOutput");
        output.attr("number", sectionNum);
        output.attr("eta", xi[sectionNum - 1] * L);

        if (strcmp(argv[2], "dsdh") != 0) {
          theResponse = section->setResponse(&argv[2], argc - 2, output);
        } else {
          theResponse       = new ElementResponse(this, 76, Vector(nsr));
          Information& info = theResponse->getInformation();
          info.theInt       = sectionNum;
        }

        output.endTag();

      } else if (sectionNum == 0) { 
        // argv[1] was not an int, we want all sections,

        CompositeResponse* theCResponse = new CompositeResponse();
        int numResponse                 = 0;
        double L = theCoordTransf->getInitialLength();
        stencil->getSectionLocations(numSections, L, xi);

        for (int i = 0; i < points.size(); i++) {

          output.tag("GaussPointOutput");
          output.attr("number", i + 1);
          output.attr("eta", xi[i] * L);

          Response* theSectionResponse = points[i].material->setResponse(&argv[1], argc - 1, output);

          if (theSectionResponse != 0) {
            numResponse = theCResponse->addResponse(theSectionResponse);
          }

          output.endTag();
        }

        if (numResponse == 0) // no valid responses found
          delete theCResponse;
        else
          theResponse = theCResponse;
      }
    }
  }

  if (theResponse == nullptr)
    theResponse = theCoordTransf->setResponse(argv, argc, output);

  output.endTag(); // ElementOutput

  return theResponse;
}

int
ForceDeltaFrame3d::getResponse(int responseID, Information& info)
{
  static Vector vp(6);

  if (responseID == 1)
    return info.setVector(this->getResistingForce());

  else if (responseID == 2) {
    THREAD_LOCAL VectorND<12> v_resp{0.0};
    THREAD_LOCAL Vector v_wrap(v_resp);

    double p0[5];
    p0[0] = p0[1] = p0[2] = p0[3] = p0[4] = 0.0;
    if (eleLoads.size() > 0)
      this->computeReactions(p0);

    // Axial
    double N     = q_pres[0];
    v_resp(6) =  N;
    v_resp(0) = -N + p0[0];

    // Torsion
    double T     = q_pres[5];
    v_resp(9) =  T;
    v_resp(3) = -T;

    // Moments about z and shears along y
    double M1     = q_pres[1];
    double M2     = q_pres[2];
    v_resp(5)  = M1;
    v_resp(11) = M2;
    double L      = theCoordTransf->getInitialLength();
    double V      = (M1 + M2) / L;
    v_resp(1)  =  V + p0[1];
    v_resp(7)  = -V + p0[2];

    // Moments about y and shears along z
    M1            = q_pres[3];
    M2            = q_pres[4];
    v_resp(4)  = M1;
    v_resp(10) = M2;
    V             = (M1 + M2) / L;
    v_resp(2)  = -V + p0[3];
    v_resp(8)  =  V + p0[4];

    return info.setVector(v_wrap);

  }


  else if (responseID == 7)
    return info.setVector(q_pres);


  // Chord rotation
  else if (responseID == 3) {
    vp = theCoordTransf->getBasicTrialDisp();
    return info.setVector(vp);
  }

  // Plastic rotation
  else if (responseID == 4) {
    static Matrix fe(6, 6);
    this->getInitialFlexibility(fe);
    vp = theCoordTransf->getBasicTrialDisp();
    vp.addMatrixVector(1.0, fe, q_pres, -1.0);
    static Vector v0(6);
    this->getInitialDeformations(v0);
    vp.addVector(1.0, v0, -1.0);
    return info.setVector(vp);
  }

  // Point of inflection
  else if (responseID == 5) {
    double LI = 0.0;

    if (fabs(q_pres[1] + q_pres[2]) > DBL_EPSILON) {
      double L = theCoordTransf->getInitialLength();

      LI = q_pres[1] / (q_pres[1] + q_pres[2]) * L;
    }

    return info.setDouble(LI);
  }

  // Tangent drift
  else if (responseID == 6) {
    double d2 = 0.0;
    double d3 = 0.0;

    int numSections = points.size();
    double L = theCoordTransf->getInitialLength();

    // Location of inflection point from node I
    double LI = 0.0;
    if (fabs(q_pres[1] + q_pres[2]) > DBL_EPSILON)
      LI = q_pres[1] / (q_pres[1] + q_pres[2]) * L;

    int i;
    for (int i = 0; i < numSections; i++) {
      double x = xi[i] * L;
      if (x > LI)
        continue;
      const ID& type = points[i].material->getType();
      int order      = points[i].material->getOrder();
      double kappa   = 0.0;
      for (int j = 0; j < nsr; j++)
        if (type(j) == SECTION_RESPONSE_MZ)
          kappa += points[i].es[j];
      double b = -LI + x;
      d2 += (wt[i] * L) * kappa * b;
    }

    d2 += stencil->getTangentDriftI(L, LI, q_pres[1], q_pres[2]);

    for (int i = numSections - 1; i >= 0; i--) {
      double x = xi[i] * L;
      if (x < LI)
        continue;
      const ID& type = points[i].material->getType();
      double kappa   = 0.0;
      for (int j = 0; j < nsr; j++)
        if (type(j) == SECTION_RESPONSE_MZ)
          kappa += points[i].es[j];
      double b = x - LI;
      d3 += (wt[i] * L) * kappa * b;
    }

    d3 += stencil->getTangentDriftJ(L, LI, q_pres[1], q_pres[2]);

    static Vector d(2);
    d(0) = d2;
    d(1) = d3;

    return info.setVector(d);
  }

  else if (responseID == 7)
    return info.setVector(q_pres);

  /*
  // Curvature sensitivity
  else if (responseID == 7) {
    Vector curv(numSections);
    for (int i = 0; i < numSections; i++) {
      int order = points[i].material->getOrder();
      const ID &type = points[i].material->getType();
      const Vector &dedh = points[i].material->getdedh();
      for (int j = 0; j < nsr; j++) {
        if (type(j) == SECTION_RESPONSE_MZ)
          curv(i) = dedh(j);
      }
    }
    return info.setVector(curv);
  }
  */

  else if (responseID == 10) {
    // ensure we have L, xi[] and wt[]
    if (this->setState(State::Init) != 0)
      return -1;

    double L = theCoordTransf->getInitialLength();

    Vector locs(points.size());
    for (int i = 0; i < points.size(); i++)
      locs[i] = xi[i] * L;

    return info.setVector(locs);
  }

  else if (responseID == 11) {
    // ensure we have L, xi[] and wt[]
    if (this->setState(State::Init) != 0)
      return -1;

    double L = theCoordTransf->getInitialLength();

    Vector weights(points.size());
    for (int i = 0; i < points.size(); i++)
      weights[i] = wt[i] * L;

    return info.setVector(weights);
  }

  else if (responseID == 110) {
    int numSections = points.size();
    ID tags(numSections);
    for (int i = 0; i < numSections; i++)
      tags(i) = points[i].material->getTag();
    return info.setID(tags);
  }

  else if (responseID == 111) {
    int numSections = points.size();
    double L = theCoordTransf->getInitialLength();
    double pts[maxNumSections];
    stencil->getSectionLocations(numSections, L, pts);
    // CBDI influence matrix
    Matrix ls(numSections, numSections);
    getCBDIinfluenceMatrix(numSections, pts, L, ls);
    // Curvature vector
    Vector kappaz(numSections); // about section z
    Vector kappay(numSections); // about section y
    for (int i = 0; i < numSections; i++) {
      const ID& code  = points[i].material->getType();
      const Vector& e = points[i].material->getSectionDeformation();
      int order       = points[i].material->getOrder();
      for (int j = 0; j < nsr; j++) {
        if (scheme[j] == SECTION_RESPONSE_MZ)
          kappaz(i) += e(j);
        if (scheme[j] == SECTION_RESPONSE_MY)
          kappay(i) += e(j);
      }
    }
    // Displacement vector
    Vector dispsy(numSections); // along local y
    Vector dispsz(numSections); // along local z
    dispsy.addMatrixVector(0.0, ls, kappaz, 1.0);
    dispsz.addMatrixVector(0.0, ls, kappay, 1.0);
    stencil->getSectionLocations(numSections, L, pts);
    static Vector uxb(3);
    static Vector uxg(3);
    Matrix disps(numSections, 3);
    vp = theCoordTransf->getBasicTrialDisp();
    for (int i = 0; i < numSections; i++) {
      uxb(0)      = pts[i] * vp(0); // linear shape function
      uxb(1)      = dispsy(i);
      uxb(2)      = dispsz(i);
      uxg         = theCoordTransf->getPointGlobalDisplFromBasic(pts[i], uxb);
      disps(i, 0) = uxg(0);
      disps(i, 1) = uxg(1);
      disps(i, 2) = uxg(2);
    }
    return info.setMatrix(disps);
  }

  else if (responseID == 112) {
    int numSections = points.size();
    double L = theCoordTransf->getInitialLength();
    double ipts[maxNumSections];
    stencil->getSectionLocations(numSections, L, ipts);
    // CBDI influence matrix
    double pts[20];
    for (int i = 0; i < 20; i++)
      pts[i] = 1.0 / (20 - 1) * i;
    Matrix ls(20, numSections);
    getCBDIinfluenceMatrix(20, pts, numSections, ipts, L, ls);
    // Curvature vector
    Vector kappaz(numSections); // about section z
    Vector kappay(numSections); // about section y
    for (int i = 0; i < numSections; i++) {
      const ID& code  = points[i].material->getType();
      const Vector& e = points[i].material->getSectionDeformation();
      int order       = points[i].material->getOrder();
      for (int j = 0; j < nsr; j++) {
        if (scheme[j] == SECTION_RESPONSE_MZ)
          kappaz(i) += e(j);
        if (scheme[j] == SECTION_RESPONSE_MY)
          kappay(i) += e(j);
      }
    }
    // Displacement vector
    Vector dispsy(20); // along local y
    Vector dispsz(20); // along local z
    dispsy.addMatrixVector(0.0, ls, kappaz, 1.0);
    dispsz.addMatrixVector(0.0, ls, kappay, 1.0);
    static Vector uxb(3);
    static Vector uxg(3);
    Matrix disps(20, 3);
    vp = theCoordTransf->getBasicTrialDisp();
    for (int i = 0; i < 20; i++) {
      uxb(0)      = pts[i] * vp(0); // linear shape function
      uxb(1)      = dispsy(i);
      uxb(2)      = dispsz(i);
      uxg         = theCoordTransf->getPointGlobalDisplFromBasic(pts[i], uxb);
      disps(i, 0) = uxg(0);
      disps(i, 1) = uxg(1);
      disps(i, 2) = uxg(2);
    }
    return info.setMatrix(disps);
  }

  return -1;
}

int
ForceDeltaFrame3d::getResponseSensitivity(int responseID, int igrad, Information& info)
{
  // Basic deformation sensitivity
  if (responseID == 3) {
    const Vector& dvdh = theCoordTransf->getBasicDisplTotalGrad(igrad);
    return info.setVector(dvdh);
  }

  // Basic force sensitivity
  else if (responseID == 7) {
    static Vector dqdh(6);

    const Vector& dvdh = theCoordTransf->getBasicDisplTotalGrad(igrad);

    dqdh.addMatrixVector(0.0, K_pres, dvdh, 1.0);

    dqdh.addVector(1.0, this->getBasicForceGrad(igrad), 1.0);

    return info.setVector(dqdh);
  }

  // dsdh
  else if (responseID == 76) {
    int numSections = points.size();

    int sectionNum = info.theInt;

    VectorND<nsr> dsdh;
    dsdh.zero();

    if (eleLoads.size() > 0) {
      this->getStressGrad(dsdh, sectionNum - 1, igrad);
    }

    static Vector dqdh(nq);
    const Vector& dvdh = theCoordTransf->getBasicDisplTotalGrad(igrad);

    dqdh.addMatrixVector(0.0, K_pres, dvdh, 1.0);

    dqdh.addVector(1.0, this->getBasicForceGrad(igrad), 1.0);

    double L        = theCoordTransf->getInitialLength();
    double oneOverL = 1.0 / L;
    double pts[maxNumSections];
    stencil->getSectionLocations(numSections, L, pts);

    double xL  = pts[sectionNum - 1];
    double xL1 = xL - 1.0;

    Vector kappa(numSections);
    Vector gamma(numSections);

    bool isGamma = false;

    for (int i = 0; i < numSections; i++) {
      int order      = points[i].material->getOrder();
      const ID& code = points[i].material->getType();
      for (int j = 0; j < nsr; j++) {
        if (scheme[j] == SECTION_RESPONSE_MZ)
          kappa(i) += (points[i].es)(j);
        if (scheme[j] == SECTION_RESPONSE_VY) {
          isGamma = true;
          gamma(i) += (points[i].es)(j);
        }
      }
    }

    isGamma = shear_flag && isGamma;

    double wi[maxNumSections];
    Vector w(wi, numSections);
    double wpi[maxNumSections];
    Vector wp(wpi, numSections);
    wp.Zero();
    this->computew(w, wp, pts, kappa, gamma);

    Matrix Ginv(numSections, numSections);
    vandermonde_inverse(numSections, pts, Ginv);

    Matrix ls(numSections, numSections);
    Matrix Hk(numSections, numSections);
    this->getHk(numSections, pts, Hk);
    ls.addMatrixProduct(0.0, Hk, Ginv, 1.0);

    Matrix lsg(numSections, numSections);
    Matrix Hg(numSections, numSections);
    this->getHg(numSections, pts, Hg);
    lsg.addMatrixProduct(0.0, Hg, Ginv, 1.0);

    Matrix lskp(numSections, numSections);
    Matrix Hkp(numSections, numSections);
    this->getHkp(numSections, pts, Hkp);
    lskp.addMatrixProduct(0.0, Hkp, Ginv, 1.0);

    Matrix lsgp(numSections, numSections);
    Matrix Hgp(numSections, numSections);
    this->getHgp(numSections, pts, Hgp);
    lsgp.addMatrixProduct(0.0, Hgp, Ginv, 1.0);

    Matrix dwidq(2 * numSections, nq);
    this->computedwdq(dwidq, q_pres, w, wp, ls, lsg, lskp, lsgp);

    double dwidh[2 * maxNumSections];
    this->computedwdh(dwidh, igrad, q_pres);

    for (int ii = 0; ii < nsr; ii++) {
      switch (scheme[ii]) {
      case SECTION_RESPONSE_P: dsdh(ii) += dqdh(0); break;
      case SECTION_RESPONSE_MZ:
        dsdh(ii) += xL1 * dqdh(1) + xL * dqdh(2);
        dsdh(ii) += wi[sectionNum - 1] * dqdh(0);
        for (int jj = 0; jj < nq; jj++)
          dsdh(ii) += q_pres[0] * dwidq(sectionNum - 1, jj) * dqdh(jj);
        dsdh(ii) += q_pres[0] * dwidh[sectionNum - 1];
        break;
      case SECTION_RESPONSE_VY:
        dsdh(ii) -= oneOverL * (dqdh(1) + dqdh(2));
        dsdh(ii) -= wpi[sectionNum - 1] * dqdh(0);
        for (int jj = 0; jj < nq; jj++)
          dsdh(ii) -= q_pres[0] * dwidq(numSections + sectionNum - 1, jj) * dqdh(jj);
        dsdh(ii) -= q_pres[0] * dwidh[numSections + sectionNum - 1];
        break;
      default: dsdh(ii) += 0.0; break;
      }
    }

    double dLdh   = theCoordTransf->getLengthGrad();
    double d1oLdh = theCoordTransf->getd1overLdh();

    double dptsdh[maxNumSections];
    stencil->getLocationsDeriv(numSections, L, dLdh, dptsdh);
    double dxLdh = dptsdh[sectionNum - 1]; // - xL/L*dLdh;

    for (int j = 0; j < nsr; j++) {
      switch (scheme[j]) {
      case SECTION_RESPONSE_MZ:
        dsdh(j) += dxLdh * (q_pres[1] + q_pres[2]);
        //dsdh(j) -= dLdh*xL/L*(q_pres[1]+q_pres[2]);
        //dsdh(j) -= dxLdh*ti[sectionNum-1]*q_pres[0];
        break;
      case SECTION_RESPONSE_VY: dsdh(j) -= d1oLdh * (q_pres[1] + q_pres[2]); break;
      default:                  break;
      }
    }

    /*

    dsdh.Zero();
    if (eleLoads.size() > 0) {
      this->getStressGrad(dsdh, sectionNum-1, igrad);
    }
    const Matrix &ks = sections[sectionNum-1]->getSectionTangent();
    const Vector &dedh  = sections[sectionNum-1]->getSectionDeformationSensitivity(igrad);
    dsdh.addMatrixVector(1.0, ks, dedh, 1.0);
    dsdh.addVector(1.0, sections[sectionNum-1]->getStressResultantSensitivity(igrad, true), 1.0);

    */

    return info.setVector(dsdh);
  }

  // Plastic deformation sensitivity
  else if (responseID == 4) {
    static Vector dvpdh(6);

    const Vector& dvdh = theCoordTransf->getBasicDisplTotalGrad(igrad);

    dvpdh = dvdh;

    static Matrix fe(6, 6);
    this->getInitialFlexibility(fe);

    const Vector& dqdh = this->getBasicForceGrad(igrad);

    dvpdh.addMatrixVector(1.0, fe, dqdh, -1.0);

    static Matrix fek(6, 6);
    fek.addMatrixProduct(0.0, fe, K_pres, 1.0);

    dvpdh.addMatrixVector(1.0, fek, dvdh, -1.0);

    const Matrix& dfedh = this->computedfedh(igrad);

    dvpdh.addMatrixVector(1.0, dfedh, q_pres, -1.0);

    return info.setVector(dvpdh);
  }

  else
    return -1;
}

int
ForceDeltaFrame3d::setParameter(const char** argv, int argc, Parameter& param)
{
  if (argc < 1)
    return -1;

  int result = -1;

  if (strcmp(argv[0], "density") == 0)
    return param.addObject(1, this);

  // section response -
  else if (strstr(argv[0], "sectionX") != 0) {
    int numSections = points.size();
    if (argc > 2) {
      float sectionLoc = atof(argv[1]);

      double xi[maxNumSections];
      double L = theCoordTransf->getInitialLength();
      stencil->getSectionLocations(numSections, L, xi);

      sectionLoc /= L;

      float minDistance = fabs(xi[0] - sectionLoc);
      int sectionNum    = 0;
      for (int i = 1; i < numSections; i++) {
        if (fabs(xi[i] - sectionLoc) < minDistance) {
          minDistance = fabs(xi[i] - sectionLoc);
          sectionNum  = i;
        }
      }

      return points[sectionNum].material->setParameter(&argv[2], argc - 2, param);
    }
  }

  // If the parameter belongs to a section or lower
  else if (strstr(argv[0], "section") != 0) {

    if (argc < 3)
      return -1;

    // Get section number: 1...Np
    int sectionNum = atoi(argv[1]);

    if (sectionNum > 0 && sectionNum <= points.size())
      return points[sectionNum - 1].material->setParameter(&argv[2], argc - 2, param);

    else
      return -1;

    /*
    // Find the right section and call its setParameter method
    int ok = 0;
    for (int i = 0; i < numSections; i++)
      if (paramSectionTag == points[i].material->getTag())
        ok += points[i].material->setParameter(&argv[2], argc-2, param);

    return ok;
    */
  }

  else if (strstr(argv[0], "integration") != 0) {

    if (argc < 2)
      return -1;

    return stencil->setParameter(&argv[1], argc - 1, param);
  }

  // Default, send to everything
  int ok;

  for (int i = 0; i < points.size(); i++) {
    ok = points[i].material->setParameter(argv, argc, param);
    if (ok != -1)
      result = ok;
  }

  ok = stencil->setParameter(argv, argc, param);
  if (ok != -1)
    result = ok;

  return result;
}


int
ForceDeltaFrame3d::updateParameter(int parameterID, Information& info)
{
  if (parameterID == 1) {
    density = info.theDouble;
    return 0;
  } else
    return -1;
}

int
ForceDeltaFrame3d::activateParameter(int passedParameterID)
{
  parameterID = passedParameterID;

  return 0;
}

const Matrix&
ForceDeltaFrame3d::getKiSensitivity(int igrad)
{
  static MatrixND<12,12> dKi{};
  static Matrix wrapper(dKi);
  return wrapper;
}

const Matrix&
ForceDeltaFrame3d::getMassSensitivity(int igrad)
{
  static MatrixND<12,12> dM{};
  static Matrix wrapper(dM);
  return wrapper;
}

const Vector&
ForceDeltaFrame3d::getResistingForceSensitivity(int igrad)
{
  VectorND<6> dqdh = this->getBasicForceGrad(igrad);

  // Transform forces
  double dp0dh[6];
  dp0dh[0] = 0.0;
  dp0dh[1] = 0.0;
  dp0dh[2] = 0.0;
  dp0dh[3] = 0.0;
  dp0dh[4] = 0.0;
  dp0dh[5] = 0.0;
  this->addReactionGrad(dp0dh, igrad);
  Vector dp0dhVec(dp0dh, 3);

  static Vector P(12);
  P.Zero();

  if (theCoordTransf->isShapeSensitivity()) {
    // dAdh^T q
    P = theCoordTransf->getGlobalResistingForceShapeSensitivity(q_pres, dp0dhVec, igrad);
    // k dAdh u
    const Vector& dAdh_u = theCoordTransf->getBasicDisplFixedGrad();
    dqdh.addMatrixVector(1.0, K_pres, dAdh_u, 1.0);
  }

  // A^T (dqdh + k dAdh u)
  P += theCoordTransf->getGlobalResistingForce(dqdh, dp0dhVec);

  return P;
}

int
ForceDeltaFrame3d::commitSensitivity(int igrad, int numGrads)
{
  int err = 0;
  int numSections = points.size();

  double L        = theCoordTransf->getInitialLength();
  double oneOverL = 1.0 / L;

  double pts[maxNumSections];
  stencil->getSectionLocations(numSections, L, pts);

  double wts[maxNumSections];
  stencil->getSectionWeights(numSections, L, wts);

  double dLdh = theCoordTransf->getLengthGrad();

  double dptsdh[maxNumSections];
  stencil->getLocationsDeriv(numSections, L, dLdh, dptsdh);

  double d1oLdh = theCoordTransf->getd1overLdh();

  static Vector dqdh(3);
  dqdh = this->getBasicForceGrad(igrad);

  // dvdh = A dudh + dAdh u
  const Vector& dvdh = theCoordTransf->getBasicDisplTotalGrad(igrad);
  dqdh.addMatrixVector(1.0, K_pres, dvdh, 1.0);

  bool isGamma = false;

  Vector kappa(numSections);
  Vector gamma(numSections);
  for (int i = 0; i < numSections; i++) {
    int order      = points[i].material->getOrder();
    const ID& code = points[i].material->getType();
    for (int j = 0; j < nsr; j++) {
      if (scheme[j] == SECTION_RESPONSE_MZ)
        kappa(i) += (points[i].es)(j);
      if (scheme[j] == SECTION_RESPONSE_VY) {
        gamma(i) += (points[i].es)(j);
        isGamma = true;
      }
    }
  }
  isGamma = shear_flag && isGamma;

  double wi[maxNumSections];
  Vector w(wi, numSections);
  double wpi[maxNumSections];
  Vector wp(wpi, numSections);
  wp.Zero();
  this->computew(w, wp, pts, kappa, gamma);

  Matrix Ginv(numSections, numSections);
  vandermonde_inverse(numSections, pts, Ginv);

  Matrix ls(numSections, numSections);
  Matrix Hk(numSections, numSections);
  this->getHk(numSections, pts, Hk);
  ls.addMatrixProduct(0.0, Hk, Ginv, 1.0);

  Matrix lsg(numSections, numSections);
  Matrix Hg(numSections, numSections);
  this->getHg(numSections, pts, Hg);
  lsg.addMatrixProduct(0.0, Hg, Ginv, 1.0);

  Matrix lskp(numSections, numSections);
  Matrix Hkp(numSections, numSections);
  this->getHkp(numSections, pts, Hkp);
  lskp.addMatrixProduct(0.0, Hkp, Ginv, 1.0);

  Matrix lsgp(numSections, numSections);
  Matrix Hgp(numSections, numSections);
  this->getHgp(numSections, pts, Hgp);
  lsgp.addMatrixProduct(0.0, Hgp, Ginv, 1.0);

  Matrix dwidq(2 * numSections, nq);
  this->computedwdq(dwidq, q_pres, w, wp, ls, lsg, lskp, lsgp);

  double dwidh[2 * maxNumSections];
  this->computedwdh(dwidh, igrad, q_pres);

  // Loop over integration points
  for (int i = 0; i < numSections; i++) {

    int order      = points[i].material->getOrder();
    const ID& code = points[i].material->getType();

    double xL  = pts[i];
    double xL1 = xL - 1.0;

    double dxLdh = dptsdh[i]; // - xL/L*dLdh;

    VectorND<nsr> ds;
    ds.zero();

    // Add sensitivity wrt element loads
    if (eleLoads.size() > 0)
      this->getStressGrad(ds, i, igrad);

    for (int j = 0; j < nsr; j++) {
      switch (scheme[j]) {
      case SECTION_RESPONSE_P: ds(j) += dqdh(0); break;
      case SECTION_RESPONSE_MZ:
        ds(j) += xL1 * dqdh(1) + xL * dqdh(2);
        ds(j) += wi[i] * dqdh(0);
        break;
      case SECTION_RESPONSE_VY:
        ds(j) -= oneOverL * (dqdh(1) + dqdh(2));
        ds(j) -= wpi[i] * dqdh(0);
        break;
      default: break;
      }
    }

    const Vector& dsdh = points[i].material->getStressResultantSensitivity(igrad, true);
    ds -= dsdh;

    for (int j = 0; j < nsr; j++) {
      switch (scheme[j]) {
      case SECTION_RESPONSE_MZ:
        ds(j) += dxLdh * (q_pres[1] + q_pres[2]);
        ds(j) +=
            (dwidq(i, 0) * dqdh(0) + dwidq(i, 1) * dqdh(1) + dwidq(i, 2) * dqdh(2) + dwidh[i]) *
            q_pres[0];
        break;
      case SECTION_RESPONSE_VY:
        ds(j) -= d1oLdh * (q_pres[1] + q_pres[2]);
        ds(j) -= (dwidq(i + numSections, 0) * dqdh(0) + dwidq(i + numSections, 1) * dqdh(1) +
                  dwidq(i + numSections, 2) * dqdh(2) + dwidh[i + numSections]) *
                 q_pres[0];
        break;
      default: break;
      }
    }

    Vector de(order);
    const Matrix& fs = points[i].material->getSectionFlexibility();
    de.addMatrixVector(0.0, fs, ds, 1.0);

    err += points[i].material->commitSensitivity(de, igrad, numGrads);
  }

  return err;
}


VectorND<6>
ForceDeltaFrame3d::getBasicForceGrad(int igrad)
{
  int numSections = points.size();

  double L        = theCoordTransf->getInitialLength();
  double oneOverL = 1.0 / L;

  double pts[maxNumSections];
  stencil->getSectionLocations(numSections, L, pts);

  double wts[maxNumSections];
  stencil->getSectionWeights(numSections, L, wts);

  double dLdh = theCoordTransf->getLengthGrad();

  double dptsdh[maxNumSections];
  stencil->getLocationsDeriv(numSections, L, dLdh, dptsdh);

  double dwtsdh[maxNumSections];
  stencil->getWeightsDeriv(numSections, L, dLdh, dwtsdh);

  double d1oLdh = theCoordTransf->getd1overLdh();

  static Vector dvdh(nq);
  dvdh.Zero();

  Vector kappa(numSections);
  Vector gamma(numSections);
  for (int i = 0; i < numSections; i++) {
    int order      = points[i].material->getOrder();
    const ID& code = points[i].material->getType();
    for (int j = 0; j < nsr; j++) {
      if (scheme[j] == SECTION_RESPONSE_MZ)
        kappa(i) += (points[i].es)(j);
      if (scheme[j] == SECTION_RESPONSE_VY)
        gamma(i) += (points[i].es)(j);
    }
  }

  double wi[maxNumSections];
  Vector w(wi, numSections);
  double wpi[maxNumSections];
  Vector wp(wpi, numSections);
  wp.Zero();
  this->computew(w, wp, pts, kappa, gamma);

  Matrix Ginv(numSections, numSections);
  vandermonde_inverse(numSections, pts, Ginv);

  double dwidh[2 * maxNumSections];
  this->computedwdh(dwidh, igrad, q_pres);

  // Loop over the integration points
  for (int i = 0; i < numSections; i++) {

    int order      = points[i].material->getOrder();
    const ID& code = points[i].material->getType();

    double xL  = pts[i];
    double xL1 = xL - 1.0;
    double wtL = wts[i] * L;

    double dxLdh  = dptsdh[i]; // - xL/L*dLdh;
    double dwtLdh = wts[i] * dLdh + dwtsdh[i] * L;

    // Get section stress resultant gradient
    Vector dsdh(order);
    dsdh = points[i].material->getStressResultantSensitivity(igrad, true);


    VectorND<nsr> dspdh;
    dspdh.zero();
    // Add sensitivity wrt element loads
    if (eleLoads.size() > 0)
      this->getStressGrad(dspdh, i, igrad);

    dsdh.addVector(1.0, dspdh, -1.0);


    for (int j = 0; j < nsr; j++) {
      switch (scheme[j]) {
      case SECTION_RESPONSE_MZ:
        dsdh(j) -= dxLdh * (q_pres[1] + q_pres[2]);
        //dsdh(j) += ti[i]*dxLdh*q_pres[0];
        dsdh(j) -= dwidh[i] * q_pres[0];
        //dsdh(j) += (2*wi[i]*oneOverL)*q_pres[0]*dLdh;
        break;
      case SECTION_RESPONSE_VY:
        dsdh(j) += d1oLdh * (q_pres[1] + q_pres[2]);
        dsdh(j) += dwidh[i + numSections] * q_pres[0];
        break;
      default: break;
      }
    }

    Vector dedh(order);
    const Matrix& fs = points[i].material->getSectionFlexibility();
    dedh.addMatrixVector(0.0, fs, dsdh, 1.0);

    for (int j = 0; j < nsr; j++) {
      double dei = dedh(j) * wtL;
      switch (scheme[j]) {
      case SECTION_RESPONSE_P: dvdh(0) += dei; break;
      case SECTION_RESPONSE_MZ:
        dvdh(1) += xL1 * dei;
        dvdh(2) += xL * dei;
        dvdh(0) += 0.5 * wi[i] * dei;
        break;
      case SECTION_RESPONSE_VY:
        dei = oneOverL * dei;
        dvdh(1) -= dei;
        dvdh(2) -= dei;
        dvdh(0) -= 0.5 * wpi[i] * dei;
      default: break;
      }
    }

    const Vector& e = points[i].es;
    for (int j = 0; j < nsr; j++) {
      switch (scheme[j]) {
      case SECTION_RESPONSE_P: dvdh(0) -= e(j) * dwtLdh; break;
      case SECTION_RESPONSE_MZ:
        dvdh(1) -= xL1 * e(j) * dwtLdh;
        dvdh(2) -= xL * e(j) * dwtLdh;
        dvdh(0) -= 0.5 * wi[i] * e(j) * dwtLdh;

        dvdh(1) -= dxLdh * e(j) * wtL;
        dvdh(2) -= dxLdh * e(j) * wtL;
        //dvdh(0) += 0.5*ti[i]*dxLdh*e(j)*wtL;
        dvdh(0) -= 0.5 * dwidh[i] * e(j) * wtL;

        //dvdh(0) += (wi[i]*oneOverL)*dLdh*e(j)*wtL;
        break;
      case SECTION_RESPONSE_VY:
        dvdh(1) += oneOverL * e(j) * dwtLdh;
        dvdh(2) += oneOverL * e(j) * dwtLdh;
        dvdh(0) += 0.5 * wpi[i] * e(j) * dwtLdh;

        dvdh(1) += d1oLdh * e(j) * wtL;
        dvdh(2) += d1oLdh * e(j) * wtL;
        dvdh(0) += 0.5 * dwidh[i + numSections] * e(j) * wtL;
        break;
      default: break;
      }
    }
  }


  VectorND<6> dqdh;
  dqdh.addMatrixVector(0.0, K_pres, dvdh, 1.0);

  return dqdh;
}

const Matrix&
ForceDeltaFrame3d::computedfedh(int igrad)
{
  int numSections = points.size();
  static Matrix dfedh(6, 6);

  dfedh.Zero();

  double L        = theCoordTransf->getInitialLength();
  double oneOverL = 1.0 / L;

  double dLdh   = theCoordTransf->getLengthGrad();
  double d1oLdh = theCoordTransf->getd1overLdh();

  double xi[maxNumSections];
  stencil->getSectionLocations(numSections, L, xi);

  double wt[maxNumSections];
  stencil->getSectionWeights(numSections, L, wt);

  double dptsdh[maxNumSections];
  stencil->getLocationsDeriv(numSections, L, dLdh, dptsdh);

  double dwtsdh[maxNumSections];
  stencil->getWeightsDeriv(numSections, L, dLdh, dwtsdh);

  for (int i = 0; i < numSections; i++) {

    int order      = points[i].material->getOrder();
    const ID& code = points[i].material->getType();

    Matrix fb(order, nq);
    Matrix fb2(order, nq);

    double xL  = xi[i];
    double xL1 = xL - 1.0;
    double wtL = wt[i] * L;

    double dxLdh  = dptsdh[i]; // - xL/L*dLdh;
    double dwtLdh = wt[i] * dLdh + dwtsdh[i] * L;

    const Matrix& fs    = points[i].material->getInitialFlexibility();
    const Matrix& dfsdh = points[i].material->getInitialFlexibilitySensitivity(igrad);
    fb.Zero();
    fb2.Zero();

    double tmp;
    for (int ii = 0; ii < nsr; ii++) {
      switch (code(ii)) {
      case SECTION_RESPONSE_P:
        for (int jj = 0; jj < nsr; jj++) {
          fb(jj, 0) += dfsdh(jj, ii) * wtL; // 1

          //fb(jj,0) += fs(jj,ii)*dwtLdh; // 3

          //fb2(jj,0) += fs(jj,ii)*wtL; // 4
        }
        break;
      case SECTION_RESPONSE_MZ:
        for (int jj = 0; jj < nsr; jj++) {
          tmp = dfsdh(jj, ii) * wtL; // 1
          fb(jj, 1) += xL1 * tmp;
          fb(jj, 2) += xL * tmp;

          tmp = fs(jj, ii) * wtL; // 2
          //fb(jj,1) += dxLdh*tmp;
          //fb(jj,2) += dxLdh*tmp;

          tmp = fs(jj, ii) * dwtLdh; // 3
          //fb(jj,1) += xL1*tmp;
          //fb(jj,2) += xL*tmp;

          tmp = fs(jj, ii) * wtL; // 4
          //fb2(jj,1) += xL1*tmp;
          //fb2(jj,2) += xL*tmp;
        }
        break;
      case SECTION_RESPONSE_VY:
        for (int jj = 0; jj < nsr; jj++) {
          tmp = oneOverL * dfsdh(jj, ii) * wtL;
          fb(jj, 1) += tmp;
          fb(jj, 2) += tmp;

          // Need to complete for dLdh != 0
        }
        break;
      default: break;
      }
    }
    for (int ii = 0; ii < nsr; ii++) {
      switch (code(ii)) {
      case SECTION_RESPONSE_P:
        for (int jj = 0; jj < nq; jj++)
          dfedh(0, jj) += fb(ii, jj);
        break;
      case SECTION_RESPONSE_MZ:
        for (int jj = 0; jj < nq; jj++) {
          tmp = fb(ii, jj); // 1,2,3
          dfedh(1, jj) += xL1 * tmp;
          dfedh(2, jj) += xL * tmp;

          tmp = fb2(ii, jj); // 4
          //dfedh(1,jj) += dxLdh*tmp;
          //dfedh(2,jj) += dxLdh*tmp;
        }
        break;
      case SECTION_RESPONSE_VY:
        for (int jj = 0; jj < nq; jj++) {
          tmp = oneOverL * fb(ii, jj);
          dfedh(1, jj) += tmp;
          dfedh(2, jj) += tmp;

          // Need to complete for dLdh != 0
        }
        break;
      default: break;
      }
    }
  }

  return dfedh;
}


int
ForceDeltaFrame3d::sendSelf(int commitTag, Channel& theChannel)
{
  int numSections = points.size();
  // place the integer data into an ID
  int dbTag = this->getDbTag();
  int loc = 0;

  static ID idData(11); // one bigger than needed so no clash later
  idData(0) = this->getTag();
  idData(1) = connectedExternalNodes(0);
  idData(2) = connectedExternalNodes(1);
  idData(3) = points.size();
  idData(4) = max_iter;
  idData(5) = state_flag;

  idData(6)          = theCoordTransf->getClassTag();
  int crdTransfDbTag = theCoordTransf->getDbTag();
  if (crdTransfDbTag == 0) {
    crdTransfDbTag = theChannel.getDbTag();
    if (crdTransfDbTag != 0)
      theCoordTransf->setDbTag(crdTransfDbTag);
  }
  idData(7) = crdTransfDbTag;

  idData(8)           = stencil->getClassTag();
  int stencilDbTag = stencil->getDbTag();
  if (stencilDbTag == 0) {
    stencilDbTag = theChannel.getDbTag();
    if (stencilDbTag != 0)
      stencil->setDbTag(stencilDbTag);
  }
  idData(9) = stencilDbTag;

  if (theChannel.sendID(dbTag, commitTag, idData) < 0) {
    opserr << "ForceDeltaFrame3d::sendSelf() - failed to send ID data\n";
    return -1;
  }

  // send the coordinate transformation
  if (theCoordTransf->sendSelf(commitTag, theChannel) < 0) {
    opserr << "ForceDeltaFrame3d::sendSelf() - failed to send crdTrans\n";
    return -1;
  }

  // send the beam integration
  if (stencil->sendSelf(commitTag, theChannel) < 0) {
    opserr << "ForceDeltaFrame3d::sendSelf() - failed to send stencil\n";
    return -1;
  }

  //
  // send an ID for the sections containing each sections dbTag and classTag
  // if section ha no dbTag get one and assign it
  //

  ID idSections(2 * numSections);
  loc = 0;
  for (int i = 0; i < numSections; i++) {
    int sectClassTag = points[i].material->getClassTag();
    int sectDbTag    = points[i].material->getDbTag();
    if (sectDbTag == 0) {
      sectDbTag = theChannel.getDbTag();
      points[i].material->setDbTag(sectDbTag);
    }

    idSections(loc)     = sectClassTag;
    idSections(loc + 1) = sectDbTag;
    loc += 2;
  }

  if (theChannel.sendID(dbTag, commitTag, idSections) < 0) {
    opserr << "ForceDeltaFrame3d::sendSelf() - failed to send ID data\n";
    return -1;
  }

  //
  // send the sections
  //

  for (int j = 0; j < numSections; j++) {
    if (points[j].material->sendSelf(commitTag, theChannel) < 0) {
      opserr << "ForceDeltaFrame3d::sendSelf() - section " << j << "failed to send itself\n";
      return -1;
    }
  }

  // into a vector place distrLoadCommit, density, UeCommit, q_past and K_past
  int secDefSize = 0;
  for (int i = 0; i < numSections; i++) {
    int size = points[i].material->getOrder();
    secDefSize += size;
  }

  Vector dData(1 + 1 + nq + nq * nq + secDefSize + 4);
  loc = 0;

  // place double variables into Vector
  dData(loc++) = density;
  dData(loc++) = tol;

  // put  distrLoadCommit into the Vector
  //  for (int i=0; i<NL; i++)
  //dData(loc++) = distrLoadcommit(i);

  // place K_past into vector
  for (int i = 0; i < nq; i++)
    dData(loc++) = q_past(i);

  // place K_past into vector
  for (int i = 0; i < nq; i++)
    for (int j = 0; j < nq; j++)
      dData(loc++) = K_past(i, j);

  // place e_past into vector
  for (int k = 0; k < points.size(); k++)
    for (int i = 0; i < nsr; i++)
      dData(loc++) = points[k].es_save[i];

  // send damping coefficients
  dData(loc++) = alphaM;
  dData(loc++) = betaK;
  dData(loc++) = betaK0;
  dData(loc++) = betaKc;

  if (theChannel.sendVector(dbTag, commitTag, dData) < 0) {
    opserr << "ForceDeltaFrame3d::sendSelf() - failed to send Vector data\n";
    return -1;
  }

  return 0;
}

int
ForceDeltaFrame3d::recvSelf(int commitTag, Channel& theChannel, FEM_ObjectBroker& theBroker)
{
  //
  // receive the integer data containing tag, numSections and coord transformation info
  //
  int dbTag = this->getDbTag();
  int i, j, k;

  static ID idData(11); // one bigger than needed

  if (theChannel.recvID(dbTag, commitTag, idData) < 0) {
    opserr << "ForceDeltaFrame3d::recvSelf() - failed to recv ID data\n";
    return -1;
  }

  this->setTag(idData(0));
  connectedExternalNodes(0) = idData(1);
  connectedExternalNodes(1) = idData(2);
  max_iter                  = idData(4);
  state_flag               = idData(5);

  int crdTransfClassTag = idData(6);
  int crdTransfDbTag    = idData(7);

  int stencilClassTag = idData(8);
  int stencilDbTag    = idData(9);

  // create a new crdTransf object if one needed
  if (theCoordTransf == 0 || theCoordTransf->getClassTag() != crdTransfClassTag) {
    if (theCoordTransf != 0)
      delete theCoordTransf;

    // TODO(cmp) - add FrameTransform to ObjBroker
    theCoordTransf = nullptr; //theBroker.getNewFrameTransform3d(crdTransfClassTag);

    if (theCoordTransf == nullptr) {
      opserr << "ForceDeltaFrame3d::recvSelf() - failed to obtain a CrdTrans object with classTag"
             << crdTransfClassTag << "\n";
      return -1;
    }
  }

  theCoordTransf->setDbTag(crdTransfDbTag);

  // invoke recvSelf on the coordTransf object
  if (theCoordTransf->recvSelf(commitTag, theChannel, theBroker) < 0) {
    opserr << "ForceDeltaFrame3d::sendSelf() - failed to recv crdTranf\n";

    return -3;
  }

  // create a new stencil object if one needed
  if (stencil == 0 || stencil->getClassTag() != stencilClassTag) {
    if (stencil != 0)
      delete stencil;

    stencil = theBroker.getNewBeamIntegration(stencilClassTag);

    if (stencil == 0) {
      opserr
          << "ForceDeltaFrame3d::recvSelf() - failed to obtain the beam integration object with classTag"
          << stencilClassTag << "\n";
      exit(-1);
    }
  }

  stencil->setDbTag(stencilDbTag);

  // invoke recvSelf on the stencil object
  if (stencil->recvSelf(commitTag, theChannel, theBroker) < 0) {
    opserr << "ForceDeltaFrame3d::sendSelf() - failed to recv beam integration\n";

    return -3;
  }

  //
  // recv an ID for the sections containing each sections dbTag and classTag
  //

  ID idSections(2 * idData(3));
  int loc = 0;

  if (theChannel.recvID(dbTag, commitTag, idSections) < 0) {
    opserr << "ForceDeltaFrame3d::recvSelf() - failed to recv ID data\n";
    return -1;
  }

  int numSections = points.size();
  //
  // now receive the sections
  //
  if (numSections != idData(3)) {

    //
    // we do not have correct number of sections, must delete the old and create
    // new ones before can recvSelf on the sections
    //


    // create a section and recvSelf on it
    numSections = idData(3);


    loc = 0;

    for (int i = 0; i < numSections; i++) {
      int sectClassTag = idSections(loc);
      int sectDbTag    = idSections(loc + 1);
      loc += 2;
      // TODO: FrameSection in object broker
//    points[i].material = theBroker.getNewSection(sectClassTag);
//    if (points[i].material == nullptr) {
//      opserr << "ForceDeltaFrame3d::recvSelf() - "
//             << "Broker could not create Section of class type " << sectClassTag << "\n";
//      exit(-1);
//    }
//    points[i].material->setDbTag(sectDbTag);
//    if (points[i].material->recvSelf(commitTag, theChannel, theBroker) < 0) {
//      opserr << "ForceDeltaFrame3d::recvSelf() - section " << i << "failed to recv itself\n";
//      return -1;
//    }
    }

    this->initializeSectionHistoryVariables();

  } else {

    //
    // for each existing section, check it is of correct type
    // (if not delete old & create a new one) then recvSelf on it
    //

    loc = 0;
    for (int i = 0; i < numSections; i++) {
      int sectClassTag = idSections(loc);
      int sectDbTag    = idSections(loc + 1);
      loc += 2;

//    // check of correct type
//    if (points[i].material->getClassTag() != sectClassTag) {
//      // delete the old section[i] and create a new one
//      delete points[i].material;
//      // TODO: FrameSection in object broker
//      points[i].material = theBroker.getNewSection(sectClassTag);
//      if (points[i].material == 0) {
//        opserr << "ForceDeltaFrame3d::recvSelf() - Broker could not create Section of class type"
//               << sectClassTag << "\n";
//        return -1;
//      }
//    }

      // recvvSelf on it
//    points[i].material->setDbTag(sectDbTag);
//    if (points[i].material->recvSelf(commitTag, theChannel, theBroker) < 0) {
//      opserr << "ForceDeltaFrame3d::recvSelf() - section " << i << "failed to recv itself\n";
//      return -1;
//    }
    }
  }

  // into a vector place distrLoadCommit, density, UeCommit, q_past and K_past
  int secDefSize = nsr*points.size();

  Vector dData(1 + 1 + nq + nq * nq + secDefSize + 4);

  if (theChannel.recvVector(dbTag, commitTag, dData) < 0) {
    opserr << "ForceDeltaFrame3d::sendSelf() - failed to send Vector data\n";
    return -1;
  }

  loc = 0;

  // place double variables into Vector
  density = dData(loc++);
  tol = dData(loc++);

  // put  distrLoadCommit into the Vector
  //for (int i=0; i<NL; i++)
  // distrLoad(i) = dData(loc++);

  // place K_past into vector
  for (int i = 0; i < nq; i++)
    q_past(i) = dData(loc++);

  // place K_past into vector
  for (int i = 0; i < nq; i++)
    for (int j = 0; j < nq; j++)
      K_past(i, j) = dData(loc++);

  K_pres = K_past;
  q_pres = q_past;

  for (int k = 0; k < points.size(); k++) {
    // place es_save into vector
    for (int i = 0; i < nsr; i++)
      points[k].es_save[i] = dData(loc++);
  }

  // set damping coefficients
  alphaM = dData(loc++);
  betaK  = dData(loc++);
  betaK0 = dData(loc++);
  betaKc = dData(loc++);

  state_flag = 2;

  return 0;
}


#if 0
void 
ForceDeltaFrame3d::zeroLoad()
{
  // This is a semi-hack -- MHS
  numEleLoads = 0;

  return;
}


int
ForceDeltaFrame3d::addLoad(ElementalLoad *theLoad, double loadFactor)
{
  if (numEleLoads == sizeEleLoads) {

    //
    // create larger arrays, copy old, delete old & set as new
    //

    ElementalLoad ** theNextEleLoads = new ElementalLoad *[sizeEleLoads+1];
    double *theNextEleLoadFactors = new double[sizeEleLoads+1];
    for (int i=0; i<numEleLoads; i++) {
      theNextEleLoads[i] = eleLoads[i];
      theNextEleLoadFactors[i] = eleLoadFactors[i];
    }
    delete [] eleLoads;
    delete [] eleLoadFactors;
    eleLoads = theNextEleLoads;
    eleLoadFactors = theNextEleLoadFactors;  

    // increment array size
    sizeEleLoads+=1;
  }

  eleLoadFactors[numEleLoads] = loadFactor;
  eleLoads[numEleLoads] = theLoad;
  numEleLoads++;

  return 0;
}

int 
ForceDeltaFrame3d::addInertiaLoadToUnbalance(const Vector &accel)
{
  // Check for a quick return
  if (density == 0.0)
    return 0;

  // get R * accel from the nodes
  const Vector &Raccel1 = theNodes[0]->getRV(accel);
  const Vector &Raccel2 = theNodes[1]->getRV(accel);    

  double L = theCoordTransf->getInitialLength();
  double m = 0.5*density*L;

  // Should be done through p0[0]
  /*
  load(0) -= m*Raccel1(0);
  load(1) -= m*Raccel1(1);
  load(2) -= m*Raccel1(2);
  load(6) -= m*Raccel2(0);
  load(7) -= m*Raccel2(1);
  load(8) -= m*Raccel2(2);
  */

  return 0;
}

const Vector &
ForceDeltaFrame3d::getResistingForceIncInertia()
{
  // Compute the current resisting force
  theVector = this->getResistingForce();

  // Check for a quick return
  if (density != 0.0) {
    const Vector &accel1 = theNodes[0]->getTrialAccel();
    const Vector &accel2 = theNodes[1]->getTrialAccel();
    
    double L = theCoordTransf->getInitialLength();
    double m = 0.5*density*L;
    
    theVector(0) += m*accel1(0);
    theVector(1) += m*accel1(1);
    theVector(2) += m*accel1(2);    
    theVector(6) += m*accel2(0);
    theVector(7) += m*accel2(1);
    theVector(8) += m*accel2(2);
    
    // add the damping forces if rayleigh damping
    if (alphaM != 0.0 || betaK != 0.0 || betaK0 != 0.0 || betaKc != 0.0)
      theVector += this->getRayleighDampingForces();

  } else {
    // add the damping forces if rayleigh damping
    if (betaK != 0.0 || betaK0 != 0.0 || betaKc != 0.0)
      theVector += this->getRayleighDampingForces();
  }

  return theVector;
}

const Matrix &
ForceDeltaFrame3d::getInitialStiff()
{
  // check for quick return
  if (Ki != nullptr)
    return *Ki;

  static Matrix f(nq, nq);   // element flexibility matrix  
  this->getInitialFlexibility(f);

  static Matrix kvInit(nq, nq);
  f.Invert(kvInit);
  Ki = new Matrix(theCoordTransf->getInitialGlobalStiffMatrix(kvInit));

  return *Ki;
}

const Matrix &
ForceDeltaFrame3d::getTangentStiff()
{
  return theCoordTransf->getGlobalStiffMatrix(K_pres, q_pres);
}

#endif
