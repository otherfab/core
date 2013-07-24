#!/usr/bin/env python

from __future__ import division
from othercore import *
import sys

def test_predicates():
  predicate_tests()

def test_constructions():
  construction_tests()

def delaunay_test(Mesh,benchmark=False,cgal=False,origin=True,circle=False):
  random.seed(8711)
  for n in range(3,10)+[50,100,563,1025,2000,-2000]+benchmark*[1<<20,-1<<20]:
    if n<0 and not origin:
      continue
    if n>0 and circle: name,X = 'circle',polar(random.uniform(0,2*pi,n))
    elif n>0:          name,X = 'gaussian',random.randn(abs(n),2)
    else:              name,X = 'origin',zeros((-n,2))
    with Log.scope('%s delaunay %s %d'%(Mesh.__name__[:-4].lower(),name,n)):
      mesh = delaunay_points(X,validate=not benchmark,Mesh=Mesh)
      if not benchmark:
        mesh.assert_consistent()
        assert mesh.n_vertices==abs(n)
        assert len(mesh.boundary_loops())==1
      if 0:
        Log.write('tris = %s'%compact_str(mesh.elements()))
        Log.write('X = %s'%compact_str(X))
    if cgal:
      from other.tim import cgal
      with Log.scope('cgal delaunay %d'%n):
        nf = cgal.cgal_time_delaunay_points(X)
        if n>0 and mesh.n_faces!=nf:
          Log.write('expected %d faces, got %d'%(mesh.n_faces,nf))

def test_delaunay_corner():
  delaunay_test(Mesh=CornerMesh)

def test_delaunay_halfedge():
  delaunay_test(Mesh=HalfedgeMesh)

def test_polygon():
  k = 4 # Use random quads to get occasional concave vertices
  verbose = False
  # We don't know how to write a unit test, so use a regression test instead
  known = {(4,5):[[[-0.969449762031,0.20665870813],[-0.511216422807,0.87163355712],[-0.586712260967,1.17031118333],[-0.690001665672,1.05665582652]],[[-0.949936673833,1.49321302481],[-0.823046918141,1.4954425225],[-0.937479680956,1.74473107309]],[[-0.915844843643,-0.0774071331925],[-0.853696540372,-1.23830703164],[-0.458037829633,-0.938758617327],[-0.823218777125,-0.689574044122]],[[0.305699187907,0.987061916812],[0.476185994327,1.16707603223],[0.306126231444,0.992095930454]],[[0.944523636191,1.11631693341],[1.51140381908,1.07802219029],[1.04704802598,1.11750647773],[0.991837294593,1.39505496663]]]
          ,(4,40):[[[-3.10894468607,-0.0724516353849],[-2.79064787844,-0.178078194819],[-2.63894001426,-0.141300181814],[-2.62490237297,-0.127368624565],[-2.62634462746,-0.138246775859],[-2.55565601136,-0.121110014759],[-2.57866438487,-0.0814806440334],[-2.00444504854,0.488394829745],[-2.59977580812,-0.0451185921597],[-2.84249122195,0.372934209372]],[[-2.54533515027,-0.903854644317],[-1.81359670755,-1.06376413137],[-2.1920738783,-0.357378380013],[-2.28605631774,-0.571542528878]],[[-2.07633025081,-0.396827687027],[-1.91174887817,-0.642060852164],[-1.76538569577,-0.591239614491]],[[-1.73342857456,0.759117478831],[-1.60481841783,0.459831002199],[-1.60727021557,0.463460193277],[-1.30987650167,-0.26973550925],[-1.24076239616,-0.374901091626],[-1.26513346113,-0.587333697594],[-1.02838108741,-0.764755776405],[-0.962353539123,-0.698407533252],[-0.947036607972,-0.715226042211],[-0.941746015094,-0.677699857507],[-0.783676946666,-0.518863075582],[-1.18742061549,0.0900555149785],[-1.21174771141,-0.121992885281],[-1.33891317093,0.0662375526884],[-1.29102110921,0.771952950583],[-1.29931032122,0.78793918832],[-1.31011623765,0.744678532752],[-1.32476281534,0.837026789331],[-1.37211677969,0.928352242155],[-1.33569191489,0.905933263233],[-1.34168217393,0.943703022492],[-1.39368185183,0.969941725023],[-1.49994037905,1.1748695826],[-1.56615322546,1.05696972707],[-1.64904360071,1.09879580528],[-1.56998935022,1.05013951967]],[[-1.46577887323,-1.07308417323],[-1.10614627715,-1.62971135477],[-1.0630088047,-1.4044464177]],[[-1.3130925233,0.39716115358],[-0.729627124778,0.589034043132],[-0.675648490868,0.554783901297],[-0.623658234916,0.126024986087],[-0.473586996325,-0.0565812525943],[-0.489134939447,-0.0485031618003],[-0.784646010476,-0.196722466059],[-0.316869103652,-0.604147321104],[-0.446928145135,-0.749018347633],[-0.126521172273,-0.887277616148],[-0.251378954812,-1.06654744176],[-0.438927872572,-1.0118548343],[-0.679384114953,-0.384932664309],[-0.657449144495,-0.892099554832],[-0.600328468618,-0.964787715629],[-0.97471477331,-0.855610481271],[-0.834672315718,-1.08044689463],[-0.46414446927,-1.37203460073],[-0.548084518251,-1.49255515097],[-0.421551375485,-1.40555297202],[-0.247617856597,-1.54243035624],[-0.208331863181,-1.52404989927],[-0.22143219609,-1.5639179591],[-0.064482244564,-1.63799254068],[0.0337400671503,-1.47800244371],[0.350227862609,-1.49693321167],[0.331836936822,-1.27132454832],[0.37752810353,-1.24994721703],[0.328939167331,-1.23577801756],[0.316467661569,-1.08278318639],[0.315047391599,-1.06538784542],[0.418373253267,-1.315915442],[0.320878524571,-0.949099490314],[0.326440957819,-0.896345010472],[0.305413285131,-0.890913088518],[0.185409545658,-0.439409614071],[0.170989094495,-0.46011449813],[0.132451970699,-0.213386734398],[0.290426819744,-0.386072369892],[0.0881102349437,-0.102225658571],[0.0897416261252,-0.0247857001863],[0.679951387719,-0.0607921611265],[0.0919990527677,0.082384312338],[0.0946954719463,0.210400886957],[0.0489509142547,0.110973962974],[0.0423105414646,0.387293592416],[0.163162604352,0.331047063043],[0.193723882833,0.256211049257],[0.205891792803,0.311160142819],[0.230521437636,0.299697133424],[0.221419845166,0.381281697811],[0.238191244433,0.457019077035],[0.736587357212,0.299462631847],[0.774631399566,0.306696586754],[1.17245390356,-0.533546992059],[1.05065266763,-0.0898494190743],[1.60318025909,-0.407235439324],[1.65186376363,-0.488296562691],[1.51882773859,-0.653301922566],[1.88349758209,-1.00281640371],[1.86076733024,-0.836133589847],[1.86445933424,-0.842280881195],[2.21359693785,-0.435381909896],[1.0424674459,-0.0600324737249],[0.933502379638,0.336905065987],[0.97384293223,0.344575570707],[0.911657441035,0.416482757501],[0.899986451074,0.458996637212],[1.17840926654,0.399951792142],[0.890797967395,0.492469294651],[0.886526339704,0.508029800357],[0.80516371431,0.539624351413],[0.749481105397,0.604011784502],[0.612028982936,0.614621585034],[0.580534932556,0.626851261044],[0.587609063472,0.61650667063],[0.278787236244,0.640344174718],[0.292933055352,0.704223870017],[0.272695080683,0.640814224755],[0.191769703022,0.647060969897],[0.186469339245,0.694571617593],[0.094897869141,0.68262285493],[0.0983065170686,0.654275034046],[0.0357786954461,0.659101509219],[0.0354000731077,0.67485917771],[-0.0403352123522,0.664976960197],[-0.232535078063,0.679812325609],[-0.294951581228,1.25602701911],[-0.193093099222,1.26801975082],[-0.259291638244,1.1937741785],[0.0232639185596,1.17987612148],[0.0211097842786,1.26952202655],[0.0244315409967,1.26864404148],[0.0351756913901,1.1792902165],[0.0799881751039,1.17708618084],[0.082094152811,1.25340143895],[0.288295716868,1.19889517649],[0.21868364447,1.77466354928],[0.09317958675,1.65510822428],[0.109972272619,2.26362725486],[0.0478077190652,1.61188700127],[-0.297833298528,1.28262933867],[-0.38827064642,2.11752509505],[-0.628379672924,1.64872678032],[-0.559307442698,1.48290694621],[-0.688978788865,1.5304106147],[-0.741487251427,1.4278908522],[-0.57561926075,1.12130027956],[-0.800141260535,0.953868945038],[-0.896791155423,1.06493929109]],[[-1.14752045128,0.931114614902],[-1.13972815928,0.828473065129],[-1.10436099431,0.864621204106]],[[-0.849300049525,2.20312305623],[-0.609349451171,2.05421280982],[-0.821390174295,2.3800963716],[-0.84543635687,2.31312977012]],[[-0.771587203889,0.921054427443],[-0.543246876337,0.820361823071],[-0.472238263295,0.698314918813],[-0.54217172848,0.703712991581],[-0.460324745661,0.677838952961],[-0.423734473502,0.614948561191],[-0.496914668859,0.605399601129]],[[-0.617466625561,0.51786630402],[-0.178225280467,0.239160481445],[-0.470602335624,0.575161460238],[-0.367092920639,0.54307382774],[-0.365308684679,0.622572305179],[-0.407922716106,0.617011965695],[-0.409650420435,0.66181956396],[-0.364746509023,0.647624192436],[-0.363796638051,0.689944398969],[-0.410874923463,0.693578475496],[-0.413558431097,0.763172401939],[-0.362656932468,0.740726204084],[-0.362377763923,0.753162115857],[-0.351933370755,0.735997088941],[-0.319405000917,0.721653060168],[-0.325233342204,0.692118424009],[-0.321945085711,0.686714069949],[-0.326234510396,0.687044884674],[-0.335818715488,0.638479328841],[-0.308818231791,0.629943750595],[-0.338261440251,0.626101693502],[-0.355363654244,0.53943800641],[-0.143423082835,0.47373743428],[0.0412619146195,0.387781788408],[-0.0388078114534,0.118331798923],[-0.033156393232,0.112861840256],[-0.204081173132,0.154484823349],[-0.0224017740182,-0.0441128874784],[-0.0361337257584,-0.0739598434463],[0.0311759040697,-0.265968827664],[-0.0745312652817,-0.334209833549],[-0.145683650124,-0.413465783315],[-0.17436542638,-0.212042537857],[-0.453923759898,-0.0667970765174],[-0.553876218666,0.372536394196]],[[0.0391227856478,0.519949948244],[0.076980831959,0.507981992744],[0.0422212075304,0.391010023664]],[[0.0853984614952,-0.230964581799],[0.0868194293863,-0.163504898878],[0.125090994104,-0.205340399026]],[[0.526134405184,1.29974760485],[0.576743823723,1.24009172963],[0.802745067833,0.88491850209],[1.16558391465,1.10627333474]],[[1.30833186439,-0.0866114129195],[1.78025965851,0.370372837977],[2.6390620132,0.410800630739],[1.77344061786,0.557715171014]]]}
  for n in 5,40:
    # Generate a bunch of positively oriented random k-gons 
    random.seed(71349271+1000*k+n)
    polys = random.randn(n,1,2)+polar(sort(random.uniform(2*pi,size=n*k).reshape(n,k),axis=1))*abs(random.randn(n,k,1))/2
    if verbose:
      print '\nn = %d\npolys = %s'%(n,compact_str(polys))
    new = canonicalize_polygons(polygon_union(polys))
    if verbose:
      print 'union = %s'%compact_str(new)
    # Check that degeneracies are fine
    area = polygon_area(new)
    assert allclose(area,polygon_area(polygon_union(new,new)))
    assert allclose(area,polygon_area(polygon_intersection(new,new)))
    # Compare against known data
    old = Nested(known[k,n])
    assert all(new.offsets==old.offsets)
    error = relative_error(new.flat,old.flat)
    if error>1e-6:
      print 'old =\n%s\n'%compact_str(old)
      print 'new =\n%s\n'%compact_str(new)
      print 'error = %g'%error
      assert False

if __name__=='__main__':
  Log.configure('exact tests',0,0,100)
  if '-b' in sys.argv:
    cgal = '-c' in sys.argv
    circle = '-d' in sys.argv
    Mesh = HalfedgeMesh if '-h' in sys.argv else CornerMesh
    delaunay_test(Mesh=Mesh,benchmark=True,origin=False,cgal=cgal,circle=circle)
  else:
    test_predicates()
    test_constructions()
    test_delaunay_corner()
    test_delaunay_halfedge()
