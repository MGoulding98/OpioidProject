from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import Drug, Prescriber, Statedata, Triple

# Create your views here.
def indexPageView(request) :

    return render(request, 'opioidSite/index.html')

def showPrescriberPageView(request) : 
    fName = request.GET['fname']
    lName = request.GET['lname']
    gender = request.GET['genderRadios']
    state = request.GET['state']
    specialty = request.GET['specialty']
    credential = request.GET['credential']

    # Prescriber Info
    prescriberQuery = 'SELECT * FROM pd_prescriber p WHERE'
    drugQuery = 'SELECT * FROM pd_triple t INNER JOIN pd_prescriber p ON p.npi = t.prescriberid INNER JOIN pd_drug d ON t.drugname = d.drugname WHERE'
    avgQuery = 'select p.drugname, p.id, p.npi, t.avp from (select t.id, fname, lname, gender, state, specialty, npi, d.drugname, qty from pd_prescriber p inner join pd_triple t on p.npi = t.prescriberid inner join pd_drug d on d.drugname = t.drugname where'
    

    if fName != '' :
        prescriberQuery += " fname = '" + fName + "'"
        drugQuery += " fname = '" + fName + "'"
        avgQuery += " fname = '" + fName + "'"
        
    if lName != '' :
        prescriberQuery += " AND lname = '" + lName + "'"
        drugQuery += " AND lname = '" + lName + "'"
        avgQuery += " AND lname = '" + lName + "'"

    if gender != '' :
        prescriberQuery += " AND gender = '" + gender + "'"
        drugQuery += " AND gender = '" + gender + "'"
        avgQuery += " AND gender = '" + gender + "'"

    if state != '' :
        prescriberQuery += " AND state = '" + state + "'" 
        drugQuery += " AND state = '" + state + "'"  
        avgQuery += " AND state = '" + state + "'"
 

    if specialty != '' :
        prescriberQuery += " AND specialty = '" + specialty + "'" 
        drugQuery += " AND specialty = '" + specialty + "'"
        avgQuery += " AND specialty = '" + specialty + "'"

    if credential != '' :
        prescriberQuery += " AND credential = '" + credential + "'"

    avgQuery +=') p inner join (select t.drugname, round(avg(qty),2) as AVP from pd_triple t inner join pd_prescriber p on t.prescriberid = p.npi group by 1) t on t.drugname = p.drugname'

    # Queries for the Prescriber details
    p = Prescriber.objects.raw(prescriberQuery)
    # Query to get prescriber drugs
    t = Triple.objects.raw(drugQuery)
    avgDrug = Triple.objects.raw(avgQuery)

    context = {
        "Prescriber" : p,
        "DrugQuantity" : t,
        "AvgDrug" : avgDrug
    }

    return render(request, 'opioidSite/showPrescriber.html', context)

def showPrescriberDetailsPageView(request, pre_num) : 
    npi = pre_num

    # Prescriber Info
    prescriberQuery = 'SELECT * FROM pd_prescriber p WHERE'
    drugQuery = 'SELECT * FROM pd_triple t INNER JOIN pd_prescriber p ON p.npi = t.prescriberid INNER JOIN pd_drug d ON t.drugname = d.drugname WHERE'
    avgQuery = 'select p.drugname, p.id, p.npi, t.avp from (select t.id, fname, lname, gender, state, specialty, npi, d.drugname, qty from pd_prescriber p inner join pd_triple t on p.npi = t.prescriberid inner join pd_drug d on d.drugname = t.drugname WHERE'
    
    prescriberQuery += " npi = '" + str(npi) + "'"
    drugQuery += " npi = '" + str(npi) + "'"
    avgQuery += " p.npi = '" + str(npi) + "'"

    avgQuery +=') p inner join (select t.drugname, round(avg(qty),2) as AVP from pd_triple t inner join pd_prescriber p on t.prescriberid = p.npi group by 1) t on t.drugname = p.drugname'

    # Queries for the Prescriber details
    p = Prescriber.objects.raw(prescriberQuery)
    # Query to get prescriber drugs
    t = Triple.objects.raw(drugQuery)
    avgDrug = Triple.objects.raw(avgQuery)

    context = {
        "Prescriber" : p,
        "DrugQuantity" : t,
        "AvgDrug" : avgDrug
    }

    return render(request, 'opioidSite/showPrescriber.html', context)
    
def showPrescriptionPageView(request) : 
    drugName = request.GET['drugname']
    isOpioid = request.GET['opioidRadios']
    
    # Prescription info
    sQuery = 'SELECT drugname, isopioid FROM pd_drug WHERE'
    tenQuery = 'select t.id, p.npi, lname, fname, t.drugname, t.qty from pd_prescriber p inner join pd_triple t on t.prescriberid = p.npi where'

    if drugName != '' :
        sQuery += " drugname = '" + drugName + "'"
        tenQuery += " drugname ='" + drugName + "'"
        
    if isOpioid != '' :
        sQuery += " AND isopioid = '" + isOpioid + "'"  
        

    tenQuery +='order by 6 desc limit 10'

    data = Drug.objects.raw(sQuery)
    topTen = Prescriber.objects.raw(tenQuery)

    context = {
        "Prescription" : data,
        "topTen" : topTen  
    }

    return render(request, 'opioidSite/showPrescription.html', context)
    
def showPrescriptionDetailsPageView(request, drug) : 
    drugName = drug

    # Prescription info
    sQuery = 'SELECT drugname, isopioid FROM pd_drug WHERE'
    tenQuery = 'select t.id, p.npi, lname, fname, t.drugname, t.qty from pd_prescriber p inner join pd_triple t on t.prescriberid = p.npi where'

    if drugName != '' :
        sQuery += " drugname = '" + drugName + "'"
        tenQuery += " drugname ='" + drugName + "'"
        

    tenQuery +='order by 6 desc limit 10'

    data = Drug.objects.raw(sQuery)
    topTen = Prescriber.objects.raw(tenQuery)

    context = {
        "Prescription" : data,
        "topTen" : topTen  
    }

    return render(request, 'opioidSite/showPrescription.html', context)

def searchPrescriberPageView(request) : 
    cred = Prescriber.objects.all().distinct('credential')
    Specialty = Prescriber.objects.all().distinct('specialty')

    context = {
        "Specialty" : Specialty,
        "Credential" : cred,
    }

    return render(request, 'opioidSite/searchPrescriber.html', context)

def searchPrescriptionPageView(request) :
    dQuery = 'SELECT DISTINCT drugname, isopioid FROM pd_drug ORDER BY drugname'   

    drug = Drug.objects.raw(dQuery)
    context = {
        # "Specialty" : Specialty,
        "Drug" : drug,
    } 
    return render(request, 'opioidSite/searchPrescription.html', context)

def aboutPageView(request) : 
    return render(request, 'opioidSite/about.html')

def analysisPageView(request) : 
    return render(request, 'opioidSite/analysis.html')

def addPrescriberPageView(request) : 

    cred = Prescriber.objects.all().distinct('credential')
    Specialty = Prescriber.objects.all().distinct('specialty')

    context = {
        "Specialty" : Specialty,
        "Credential" : cred,
    }

    if request.method == 'POST' :
        prescriber = Prescriber()
        state = Statedata.objects.get(stateabbrev = request.POST['state'])

        # Takes input and saves to database
        prescriber.npi = request.POST['npi']
        prescriber.fname = request.POST['fname']
        prescriber.lname = request.POST['lname']
        prescriber.gender = request.POST['genderRadios']
        prescriber.state = state
        prescriber.specialty = request.POST['specialty']
        prescriber.credential = request.POST['credential']
        prescriber.isopioidprescriber = request.POST['isOpioidPrescriberRadios']
        prescriber.totalprescriptions = request.POST['totalPrescriptions']

        prescriber.save()

        return render(request, 'opioidSit/index.html')
    else :
        return render(request, 'opioidSite/addPrescriber.html', context)

def editPrescriberPageView(request, pre_num) : 
    if request.method == 'POST' :
        prescriber = Prescriber.objects.get(npi = pre_num)
        state = Statedata.objects.get(stateabbrev = request.POST['state'])

        # Edits and saves current prescriber
        prescriber.fname = request.POST['fname']
        prescriber.lname = request.POST['lname']
        prescriber.gender = request.POST['genderRadios']
        prescriber.state = state
        prescriber.specialty = request.POST['specialty']
        prescriber.credential = request.POST['credential']
        prescriber.isopioidprescriber = request.POST['isOpioidPrescriberRadios']
        prescriber.totalprescriptions = request.POST['totalPrescriptions']

        prescriber.save()

        return render(request, 'opioidSite/index.html')
    else : 
        PrescriberInfo = Prescriber.objects.get(npi = pre_num)
        cred = Prescriber.objects.all().distinct('credential')
        Specialty = Prescriber.objects.all().distinct('specialty')
        State = Statedata.objects.all().distinct('stateabbrev')

        context = {
            "Specialty" : Specialty,
            "Credential" : cred,
            "Prescriber" : PrescriberInfo,
            "State" : State
        }
        return render(request, 'opioidSite/editPrescriber.html', context)

def deletePrescriberPageView(request, pre_num) :
    data = Prescriber.objects.get(npi = pre_num)

    data.delete()

    return render(request, 'opioidSite/index.html')

def viewAllPrescriptionsPageView(request):
    drug = Drug.objects.all()

    paginator = Paginator(drug, 10)  # 10 posts in each page
    page = request.GET.get('page')
    try:
        post_list = paginator.page(page)
    except PageNotAnInteger:
            # If page is not an integer deliver the first page
        post_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        post_list = paginator.page(paginator.num_pages)

    context = {
        "page": page,
        "post_list": post_list
    }

    return render(request, 'opioidSite/viewAllPrescriptions.html', context)

def viewAllPrescribersPageView (request):
    prescriber = Prescriber.objects.all()

    paginator = Paginator(prescriber, 10)  # 10 posts in each page
    page = request.GET.get('page')
    try:
        post_list = paginator.page(page)
    except PageNotAnInteger:
            # If page is not an integer deliver the first page
        post_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        post_list = paginator.page(paginator.num_pages)

    context = {
        "page": page,
        "post_list": post_list
    }

    return render(request, 'opioidSite/viewAllPrescribers.html', context)