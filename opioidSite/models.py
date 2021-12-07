from django.db import models
class Drug(models.Model):
    drugname = models.CharField(primary_key=True, max_length=30, verbose_name="Name of prescription")
    isopioid = models.CharField(max_length=5, verbose_name="Is it an opioid (true/false)")
    uir_triple = models.ManyToManyField('Prescriber', through='Triple')

    class Meta:
        db_table = 'pd_drug'

    def __str__(self) :
        return self.drugname

    def save(self) :
        self.drugname = self.drugname.upper()
        self.isopioid = self.isopioid.upper()

        super(Drug, self).save()


class Prescriber(models.Model):
    npi = models.IntegerField(default=0, primary_key=True, verbose_name="National Provider Identifier")
    fname = models.CharField(max_length=50, verbose_name="First Name")
    lname = models.CharField(max_length=50, verbose_name="Last Name")
    gender = models.CharField(max_length=1)
    state = models.ForeignKey('Statedata', models.DO_NOTHING, db_column='state')
    credential = models.CharField(max_length=10)
    specialty = models.CharField(max_length=62)
    isopioidprescriber = models.CharField(max_length=5, verbose_name="Do they prescribe opioids (true/false)")
    totalprescriptions = models.IntegerField(default=0, verbose_name="Total amount of prescriptions")

  
    uir_triple = models.ManyToManyField('Drug', through='Triple')

    class Meta:
        db_table = 'pd_prescriber'

    def __str__(self) :
        return (self.fname + " " + self.lname)

    def save(self):
        self.fname = self.fname.lower()
        self.lname = self.lname.lower()

        self.fname = self.fname.capitalize()
        self.lname = self.lname.capitalize()
        self.gender = self.gender.upper()
        self.credential = self.credential.upper()
        self.specialty = self.specialty.title()

        self.isopioidprescriber = self.isopioidprescriber.upper()

        super(Prescriber, self).save()




class Statedata(models.Model):
    stateabbrev = models.CharField(primary_key=True, max_length=2, verbose_name="State Abbreviation")
    state = models.CharField(max_length=50)
    population = models.IntegerField(default=0)
    deaths = models.IntegerField(default=0, verbose_name="Opioid Deaths")

    class Meta:
        db_table = 'pd_statedata'
    
    def __str__(self) :
        return self.state

    def save(self) :
        self.stateabbrev = self.stateabbrev.upper()
        
        self.state = self.state.lower()
        self.state = self.state.title()



        super(Statedata, self).save()


class Triple(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    prescriberid = models.ForeignKey(Prescriber, on_delete=models.CASCADE, db_column='prescriberid', verbose_name="Prescriber Name")
    drugname = models.ForeignKey(Drug, on_delete=models.CASCADE, db_column='drugname', verbose_name="Name of prescription")
    qty = models.IntegerField(default=0, verbose_name="Quantity Prescribed")

    class Meta:
        db_table = 'pd_triple'
    
    def __str__(self) :
        return self.qty
    

    def __str__(self) :
        return (str(self.prescriberid) + " — " + str(self.drugname))