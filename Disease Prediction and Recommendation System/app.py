from flask import Flask, render_template, redirect, request, flash, session
import db
import os
import pandas as pd
import pickle
import re
import string
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import CountVectorizer
app = Flask(__name__)
app.secret_key = 'super secret key'

login_status = ''
uname = ''
path = os.getcwd()+"/models/"
otp = ""
precautions = []
diets = []

@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/ulogin', methods=['POST'])
def user_login():
    global login_status
    global uname
    uname = uname
    login_status = login_status
    if request.method == 'POST':
        email = request.form.get('email')
        pwd = request.form.get('pwd')

        if db.check_mail_pwd(email, pwd) == True:
            data = db.get_info(email)
            uname=data[1]
            login_status = True
            session['email'] = email
            if login_status == True:
                return redirect('/user')
        else:
            flash('Invalid Login Credentials')
            return redirect('/login')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/usignup', methods=['POST', 'GET'])
def usignup():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        pwd = request.form.get('pwd')
        cpwd = request.form.get('cpwd')
        if db.exist_mail(email) == True:
            flash('Email Already Exists')
            return redirect('/signup')
        if pwd != cpwd:
            flash('Password and Confirm Password is not same')
            return redirect('/signup')
        db.insert_data(name, email, pwd)

    return redirect('/login')


@app.route('/user')
def user():
    global login_status, otp, precautions, diets
    otp = ''
    precautions = []
    diets = []
    if login_status == True:
        return render_template('user.html', name=uname)
    else:
        return redirect('/login')

@app.route('/predict1')
def predict1():
    global login_status
    global uname, otp, precautions, diets
    if login_status == True:
        return render_template('predict1.html', name=uname, output=otp, precautions=precautions, diets=diets)
    else:
        return redirect('/login')

@app.route('/predict1/predict', methods=['POST'])
def predict_breast_cancer():
    # -----------------Breast Cancer--------------------
    global otp, precautions, diets
    if request.method == 'POST':
        radius_mean = request.form.get("radius_mean")
        perimeter_mean = request.form.get("perimeter_mean")
        area_mean = request.form.get("area_mean")
        concave_points_mean = request.form.get("concave points_mean")
        radius_worst = request.form.get("radius_worst")
        perimeter_worst = request.form.get("perimeter_worst")
        area_worst = request.form.get("area_worst")
        concave_points_worst = request.form.get("concave points_worst")
        otp = 'Yes'

        model = pickle.load(open(path+'breast.pkl', 'rb'))
        l = [float(radius_mean),float(perimeter_mean),float(area_mean),float(concave_points_mean),float(radius_worst),float(perimeter_worst),float(area_worst),float(concave_points_worst)]
        result = model.predict([l])
        msg = "YES"
        if result == 1:
            msg = "YES"
        else:
            msg = "NO"

        otp = msg

        precautions = ['Regular Breast Self-Examination: Conduct a breast self-examination monthly to detect any unusual lumps or changes in your breast.', 'Mammography: Get a mammogram once every year if you are 40 years old or above, or if you are at high risk for breast cancer.', 'Maintain a Healthy Weight: Being overweight or obese can increase the risk of breast cancer, so it\'s important to maintain a healthy weight through a balanced diet and regular exercise.', 'Limit Alcohol Intake: Limiting alcohol intake can help reduce the risk of breast cancer. Women should limit their alcohol intake to no more than one drink per day.', 'Breastfeeding: Breastfeeding can reduce the risk of breast cancer, so if possible, try to breastfeed your baby for at least 6 months.']

        diets = ['There is no specific diet that can prevent or cure breast cancer, but a healthy diet can help reduce the risk of breast cancer and improve overall health. Here are some dietary recommendations that may be helpful: ', 'Eat a balanced diet: A balanced diet includes fruits, vegetables, whole grains, lean protein, and healthy fats. Avoid processed and sugary foods.', 'Increase fiber intake: High fiber foods such as whole grains, fruits, and vegetables can help reduce the risk of breast cancer.', 'Choose plant-based protein: Plant-based protein sources such as beans, lentils, and tofu are good choices.', 'Limit red meat and processed meat: Red meat and processed meat have been linked to an increased risk of breast cancer, so it\'s best to limit intake.']

        return redirect('/predict1')

@app.route('/predict2')
def predict2():
    global login_status
    global uname,otp, precautions, diets
    if login_status == True:
        return render_template('predict2.html', name=uname, output=otp, precautions=precautions, diets=diets)
    else:
        return redirect('/login')

@app.route('/predict2/predict', methods=['POST'])
def predict_diabetes():
    # ------------Diabetes Prediction------------
    global otp, precautions, diets

    if request.method == "POST":
        preg = request.form.get("preg")
        glucose = request.form.get("glucose")
        bp = request.form.get("bp")
        st = request.form.get("st")
        si = request.form.get("insulin")
        bmi = request.form.get("bmi")
        Dp = request.form.get("DiabetesPedigreeFunction")
        age = request.form.get("age")

        model = pickle.load(open(path+'diabetes.pkl', 'rb'))
        result = model.predict([[int(preg),int(glucose),int(bp),int(st),int(si),float(bmi),float(Dp),int(age)]])
        msg = "YES"
        if result == 1:
            msg = "YES"
        else:
            msg = "NO"

        otp = msg

        precautions = ['Monitor Blood Sugar Levels: Regularly check your blood sugar levels as recommended by your doctor, and take necessary measures to keep it within a healthy range.', 'Follow a Healthy Diet: Adopt a healthy diet that is low in sugar, refined carbohydrates, and unhealthy fats, and high in fiber, whole grains, fruits, and vegetables. Consult with a registered dietitian for personalized dietary advice.', 'Get Regular Physical Activity: Regular physical activity can help improve blood sugar control, reduce the risk of complications, and improve overall health. Aim for at least 30 minutes of moderate-intensity exercise most days of the week.', 'Take Medications as Prescribed: Take medications as prescribed by your doctor, and follow the recommended dosages and schedules.', 'Regular Check-ups: Regularly visit your doctor for check-ups and screenings, and take care of any health issues promptly.']

        diets = ['Emphasize non-starchy vegetables: Non-starchy vegetables, such as leafy greens, broccoli, cauliflower, carrots, and bell peppers, are low in carbohydrates and high in fiber, vitamins, and minerals. They can help fill you up without affecting blood sugar levels.', 'Choose whole grains: Whole grains, such as brown rice, quinoa, and whole-grain bread, are high in fiber and can help regulate blood sugar levels. They also provide more nutrients than refined grains.', 'Include lean protein sources: Lean protein sources, such as chicken, fish, turkey, and tofu, can help regulate blood sugar levels and provide satiety. They are also lower in fat than many other protein sources.', 'Limit added sugars: Added sugars can raise blood sugar levels and contribute to weight gain. Try to limit your intake of sugary drinks, desserts, and processed foods that contain added sugars.', 'Stay hydrated with water: Drinking enough water is important for staying hydrated and regulating blood sugar levels. Avoid sugary drinks and choose water as your primary beverage.']

        return redirect('/predict2')
    
@app.route('/predict3')
def predict3():
    global login_status
    global uname
    if login_status == True:
        return render_template('predict3.html', name=uname,output=otp, precautions=precautions, diets=diets)
    else:
        return redirect('/login')

@app.route('/predict3/predict', methods=['POST'])
def predict_heart():
    # ------------Heart Disease Prediction------------
    global otp, precautions, diets
    if request.method == "POST":
        age = request.form.get("age"),
        sex =  request.form.get("sex"),
        cp =  request.form.get("cp"),
        trestbps =  request.form.get("trestbps"),
        chol =  request.form.get("sc"),
        fbs = request.form.get("fbs"),
        restecg = request.form.get("restecg"),
        thalach = request.form.get("thalac"),
        exang = request.form.get("exang")
        oldpeak = request.form.get("oldpeak")
        slope = request.form.get("slope")	
        ca = request.form.get("ca")	
        thal =  request.form.get("thal")


        Sex = 1

        if sex == "male":
            Sex = 1
        elif sex == "female":
            Sex = 0
        else:
            Sex  = 0
        
        ex = 1

        if exang == "Yes":
            ex = 1
        else:
            ex = 0

        Ca = 1
        if ca == "Yes":
            Ca = 1
        else:
            Ca = 0

        data = pd.read_csv("heart.csv")
        X = data.drop("target", axis=1)
        y = data["target"]
        model = pickle.load(open(path+'heart.pkl', 'rb'))
        model.fit(X,y)
        result = model.predict([[int(age[0]),int(Sex),int(cp[0]),int(trestbps[0]),int(chol[0]),int(fbs[0]),int(restecg[0]),int(thalach[0]),int(ex),float(oldpeak),int(slope),int(Ca),int(thal)]])
        msg = "YES"
        if result == 1:
            msg = "YES"
        else:
            msg = "NO"

        otp = msg

        precautions = ['Maintain a Healthy Weight: Maintaining a healthy weight can help reduce the risk of heart disease. Excess weight can increase blood pressure, cholesterol levels, and the risk of developing type 2 diabetes, all of which are risk factors for heart disease.', 'Follow a Healthy Diet: A healthy diet can help reduce the risk of heart disease. A diet that is rich in fruits, vegetables, whole grains, lean proteins, and healthy fats, and low in saturated and trans fats, added sugars, and salt can help lower blood pressure, cholesterol levels, and the risk of heart disease.', 'Engage in Regular Physical Activity: Regular physical activity can help reduce the risk of heart disease by improving blood pressure, cholesterol levels, and overall heart health. Aim for at least 150 minutes of moderate-intensity exercise per week.', 'Quit Smoking: Smoking is a major risk factor for heart disease. Quitting smoking can help reduce the risk of heart disease and improve overall health.', 'Manage Chronic Conditions: Managing chronic conditions such as high blood pressure, high cholesterol, and diabetes can help reduce the risk of heart disease. It\'s important to work with a healthcare professional to monitor and manage these conditions.']

        diets = ['Eat a diet rich in fruits and vegetables: Fruits and vegetables are rich in vitamins, minerals, and fiber, which can help improve heart health. Aim for at least 5 servings of fruits and vegetables per day.', 'Choose whole grains: Whole grains, such as whole-grain bread, brown rice, and quinoa, are high in fiber and can help lower cholesterol levels and reduce the risk of heart disease.', 'Choose lean protein sources: Choose lean protein sources, such as chicken, fish, and legumes, over red meat. Red meat is high in saturated fat, which can raise cholesterol levels and increase the risk of heart disease.', 'Limit unhealthy fats: Limit saturated and trans fats, which can raise cholesterol levels and increase the risk of heart disease. Instead, choose healthy fats, such as those found in nuts, seeds, and avocados.', 'Reduce sodium intake: High sodium intake can raise blood pressure and increase the risk of heart disease. Try to limit sodium intake to less than 2,300 milligrams per day.']

        return redirect('/predict3')
    
@app.route('/predict4')
def predict4():
    global login_status
    global uname, otp, precautions, diets
    if login_status == True:
        return render_template('predict4.html', name=uname, output=otp, precautions=precautions, diets=diets)
    else:
        return redirect('/login')

@app.route('/predict4/predict', methods=['POST'])
def predict_kideny():
    global otp, precautions, diets
    if request.method == "POST":
        sg =  request.form.get("sg"),
        al =  request.form.get("al"),
        rbc = request.form.get("rbc"),
        hemo = request.form.get("hemo"),
        pkdc = request.form.get("pkdc"),
        htn = request.form.get("htn"),
        dm = request.form.get("dm")	

        Rbc = 1
        if rbc[0] == "normal":
            Rbc = 1
        else:
            Rbc = 0

        Htn = 1

        if htn[0] != "Yes":
            Htn = 0

        Dm = 1
        if  dm != "Yes":
            Dm = 0
        
        model = pickle.load(open(path+'kidney.pkl', 'rb'))
        result = model.predict([[float(sg[0]),float(al[0]),float(Rbc),float(hemo[0]),float(pkdc[0]),int(Htn),int(Dm)]])
        
        msg = "YES"
        if result == 1:
            msg = "YES"
        else:
            msg = "NO"

        otp = msg

        precautions = ['Control blood sugar and blood pressure: High blood sugar and high blood pressure can damage the kidneys over time, so it\'s important to control these conditions through medication, lifestyle changes, and regular monitoring.', 'Stay hydrated: Dehydration can put stress on the kidneys and increase the risk of kidney damage. Aim to drink enough water and other fluids to stay hydrated.', 'Limit alcohol consumption: Drinking excessive amounts of alcohol can damage the kidneys over time, so it\'s important to limit alcohol consumption or avoid it altogether.', 'Avoid over-the-counter pain medications: Over-the-counter pain medications, such as ibuprofen and naproxen, can be harmful to the kidneys when taken in high doses or for extended periods. Consult a healthcare professional before taking any new medications.', 'Quit smoking: Smoking can increase the risk of kidney disease and make existing kidney damage worse. Quitting smoking can help reduce the risk of kidney disease and improve overall health.']

        diets = ['Reduce protein intake: Eating too much protein can put stress on the kidneys and increase the risk of kidney damage. A healthcare professional can recommend an appropriate level of protein intake based on individual needs.', 'Limit sodium intake: High sodium intake can raise blood pressure and increase the risk of kidney damage. Try to limit sodium intake to less than 2,300 milligrams per day.', 'Control potassium and phosphorus intake: When the kidneys are not functioning properly, potassium and phosphorus levels can build up in the body and cause complications. A healthcare professional can recommend an appropriate level of potassium and phosphorus intake based on individual needs.', 'Choose healthy fats: Choose healthy fats, such as those found in nuts, seeds, and avocados, over saturated and trans fats, which can raise cholesterol levels and increase the risk of kidney damage.', 'Stay hydrated: Staying hydrated is important for kidney health. However, those with kidney disease may need to limit fluid intake to avoid overloading the kidneys. A healthcare professional can recommend an appropriate fluid intake based on individual needs.']

        return redirect('/predict4')
    
@app.route('/predict5')
def predict5():
    global login_status
    global uname, otp, precautions, diets
    if login_status == True:
        return render_template('predict5.html', name=uname,output=otp, precautions=precautions, diets=diets)
    else:
        return redirect('/login')
    
@app.route('/predict5/predict', methods=['POST'])
def predict_liver():
    # ------------Liver Disease Prediction------------
    global otp, precautions, diets
    if request.method == "POST":
        a =  request.form.get("a"),
        b =  request.form.get("b"),

        model = pickle.load(open(path+'liver.pkl', 'rb'))
        result = model.predict([[float(a[0]),float(b[0])]])
        
        msg = "YES"
        if result == 1:
            msg = "YES"
        else:
            msg = "NO"

        otp = msg

        # print(otp,"---------------------",result)
        precautions = ['Limit alcohol consumption: Excessive alcohol consumption can cause liver damage and increase the risk of developing liver disease. It\'s important to limit alcohol consumption or avoid it altogether.', 'Practice safe sex: Viral hepatitis, which can lead to liver disease, can be transmitted through sexual contact. Practice safe sex to reduce the risk of contracting hepatitis B or C.', 'Use caution with medications: Certain medications, including prescription and over-the-counter drugs, can cause liver damage or worsen existing liver disease. Consult a healthcare professional before taking any new medications.', 'Get vaccinated for hepatitis: Hepatitis A and B can be prevented through vaccination. Speak with a healthcare professional to determine if vaccination is recommended based on individual risk factors.', 'Maintain a healthy weight: Obesity and non-alcoholic fatty liver disease are closely linked. Maintaining a healthy weight through a balanced diet and regular exercise can help prevent or slow the progression of liver disease.']

        diets = ['Limit saturated and trans fats: Saturated and trans fats can increase the risk of non-alcoholic fatty liver disease, which can lead to liver damage. Choose healthy fats, such as those found in nuts, seeds, and avocados, instead.', 'Increase fiber intake: A diet high in fiber can help prevent or reduce the buildup of fat in the liver. Choose whole grains, fruits, vegetables, and legumes to increase fiber intake.', 'Limit sugar and refined carbohydrates: High sugar and refined carbohydrate intake can contribute to non-alcoholic fatty liver disease. Limit intake of sugary drinks, candy, baked goods, and other foods high in sugar and refined carbohydrates.', 'Increase antioxidant-rich foods: Antioxidants can help protect the liver from damage. Choose foods high in antioxidants, such as berries, leafy greens, and cruciferous vegetables.', 'Limit sodium intake: High sodium intake can contribute to fluid retention and increase the risk of complications in those with advanced liver disease. Aim to limit sodium intake to less than 2,300 milligrams per day.']
        
        return redirect('/predict5')


@app.route('/predict6')
def predict6():
    global login_status
    global uname, otp, precautions, diets
    if login_status == True:
        return render_template('predict6.html', name=uname, output=otp,precautions=precautions, diets=diets)
    else:
        return redirect('/login')

    
@app.route('/predict6/predict', methods=['POST'])
def predict_strocs():
    # ------------Strocks Prediction------------
    global otp, precautions, diets
    if request.method == "POST":
        age = request.form.get("age")
        hypertension = request.form.get("hypertension")
        heart_disease = request.form.get("heart_disease")
        avg_glucose_level = request.form.get("avg_glucose_level")
        bmi = request.form.get("bmi")
        gender = request.form.get("gender")
        ever_married = request.form.get("ever_married")
        work_type = request.form.get("work_type")
        Residence_type = request.form.get("Residence_type")
        smoking_status = request.form.get("smoking_status")
        stroke = request.form.get("stroke")

        g = [1,0,0]
        if gender == "female":
            g = [0,1,0]
        elif gender == "other":
            g = [0,0,1]
        em = [1,0]
        if em != "Yes":
            em = [0,1]

        k = ['Govt_job', 'children','Private','Self-employed']
        k1 = [0,0,0,0]
        k1[k.index(work_type)] = 1

        rs = ['Rural','Urban']
        rs1 = [0,0]
        rs1[rs.index(Residence_type)] = 1


        sm = ['Unknown','formerly smoked', 'never smoked', 'smokes' ]
        sm1 = [0,0,0,0]
        sm1[sm.index(smoking_status)] = 1

        final = [float(age), int(hypertension), int(heart_disease), float(avg_glucose_level), float(bmi)]+g+em+k1+rs1+sm1

        
        model = pickle.load(open(path+'strock.pkl', 'rb'))
        result = model.predict([final])
        
        msg = "YES"
        if result == 1:
            msg = "YES"
        else:
            msg = "NO"

        otp = msg

        precautions = ['Control blood pressure: High blood pressure is a major risk factor for stroke. Monitoring blood pressure regularly and taking medication as prescribed by a healthcare professional can help control blood pressure and reduce the risk of stroke.', 'Manage diabetes: People with diabetes are at a higher risk of stroke. Controlling blood sugar levels through medication, a healthy diet, and regular exercise can help reduce the risk of stroke.', 'Quit smoking: Smoking is a major risk factor for stroke. Quitting smoking can significantly reduce the risk of stroke and other health complications.', 'Exercise regularly and maintain a healthy weight: Regular exercise and maintaining a healthy weight can help reduce the risk of stroke. Aim for at least 150 minutes of moderate exercise per week and follow a balanced diet to maintain a healthy weight.']

        diets = ['Eat a diet rich in fruits and vegetables: A diet rich in fruits and vegetables provides important nutrients, fiber, and antioxidants that can help reduce the risk of stroke. Aim for at least five servings of fruits and vegetables per day.', 'Choose whole grains: Whole grains are a good source of fiber, vitamins, and minerals that can help reduce the risk of stroke. Choose whole-grain bread, pasta, and cereals.', 'Limit saturated and trans fats: Saturated and trans fats can contribute to high cholesterol levels and increase the risk of stroke. Limit intake of red meat, fried foods, and processed foods high in saturated and trans fats.', 'Reduce sodium intake: High sodium intake can increase blood pressure, which is a major risk factor for stroke. Aim to limit sodium intake to less than 2,300 milligrams per day.']

        return redirect('/predict6')


# @app.route('/predict7')
# def predict7():
#     global login_status
#     global uname
#     if login_status == True:
#         return render_template('predict7.html', name=uname)
#     else:
#         return redirect('/login')

@app.route('/predict8')
def predict8():
    global login_status
    global uname, otp, precautions, diets
    if login_status == True:
        return render_template('predict8.html', name=uname,output=otp, precautions=precautions, diets=diets)
    else:
        return redirect('/login')

@app.route('/predict8/predict', methods=['POST'])
def predict_depression():
    # ------------Depression Prediction------------
    global otp, precautions, diets
    if request.method == 'POST':

        intpt = request.form.get("intpt")

        def text_transformation(text):
            text = text.lower()
            text = re.sub('\[.*?\]', '', text)
            text = re.sub("\\W"," ",text) 
            text = re.sub('https?://\S+|www\.\S+', '', text)
            text = re.sub('<.*?>+', '', text)
            text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
            text = re.sub('\n', '', text)
            text = re.sub('\w*\d\w*', '', text)    
            return text
        
        contraction_mapping = {"ain't": "is not", "aren't": "are not","can't": "cannot", "'cause": "because", "could've": "could have", "couldn't": "could not",
                           "didn't": "did not",  "doesn't": "does not", "don't": "do not", "hadn't": "had not", "hasn't": "has not", "haven't": "have not",
                           "he'd": "he would","he'll": "he will", "he's": "he is", "how'd": "how did", "how'd'y": "how do you", "how'll": "how will", "how's": "how is",
                           "I'd": "I would", "I'd've": "I would have", "I'll": "I will", "I'll've": "I will have","I'm": "I am", "I've": "I have", "i'd": "i would",
                           "i'd've": "i would have", "i'll": "i will",  "i'll've": "i will have","i'm": "i am", "i've": "i have", "isn't": "is not", "it'd": "it would",
                           "it'd've": "it would have", "it'll": "it will", "it'll've": "it will have","it's": "it is", "let's": "let us", "ma'am": "madam",
                           "mayn't": "may not", "might've": "might have","mightn't": "might not","mightn't've": "might not have", "must've": "must have",
                           "mustn't": "must not", "mustn't've": "must not have", "needn't": "need not", "needn't've": "need not have","o'clock": "of the clock",
                           "oughtn't": "ought not", "oughtn't've": "ought not have", "shan't": "shall not", "sha'n't": "shall not", "shan't've": "shall not have",
                           "she'd": "she would", "she'd've": "she would have", "she'll": "she will", "she'll've": "she will have", "she's": "she is",
                           "should've": "should have", "shouldn't": "should not", "shouldn't've": "should not have", "so've": "so have","so's": "so as",
                           "this's": "this is","that'd": "that would", "that'd've": "that would have", "that's": "that is", "there'd": "there would",
                           "there'd've": "there would have", "there's": "there is", "here's": "here is","they'd": "they would", "they'd've": "they would have",
                           "they'll": "they will", "they'll've": "they will have", "they're": "they are", "they've": "they have", "to've": "to have",
                           "wasn't": "was not", "we'd": "we would", "we'd've": "we would have", "we'll": "we will", "we'll've": "we will have", "we're": "we are",
                           "we've": "we have", "weren't": "were not", "what'll": "what will", "what'll've": "what will have", "what're": "what are",
                           "what's": "what is", "what've": "what have", "when's": "when is", "when've": "when have", "where'd": "where did", "where's": "where is",
                           "where've": "where have", "who'll": "who will", "who'll've": "who will have", "who's": "who is", "who've": "who have",
                           "why's": "why is", "why've": "why have", "will've": "will have", "won't": "will not", "won't've": "will not have",
                           "would've": "would have", "wouldn't": "would not", "wouldn't've": "would not have", "y'all": "you all",
                           "y'all'd": "you all would","y'all'd've": "you all would have","y'all're": "you all are","y'all've": "you all have",
                           "you'd": "you would", "you'd've": "you would have", "you'll": "you will", "you'll've": "you will have",
                           "you're": "you are", "you've": "you have"}
        
        def text_cleaner(text):
            newString = text.lower()
            newString = BeautifulSoup(newString, "lxml").text
            newString = re.sub(r'\([^)]*\)', '', newString)
            newString = re.sub('"','', newString)
            newString = ' '.join([contraction_mapping[t] if t in contraction_mapping else t for t in newString.split(" ")])    
            newString = re.sub(r"'s\b","",newString)
            newString = re.sub("[^a-zA-Z]", " ", newString) 
            newString = re.sub('[m]{2,}', 'mm', newString)
            return newString
        
        vect = CountVectorizer(max_features = 20000 , lowercase=False , ngram_range=(1,2))
        

        text = intpt
        clean_text = text_cleaner(text)
        df = pd.read_excel("dataset.xlsx")
        df.dropna(inplace=True)
        df['cleaned'] = df["text"].apply(text_cleaner)
        
        a = vect.fit_transform(X).toarray()
        # X_cv =vect.fit_transform(X).toarray()
       

        loaded_model = pickle.load(open(path+'CV_BestModel.sav', 'rb'))
        single_prediction = int(loaded_model.predict(a)[0])
        output = {0:"No Anxiety/Depression",
                1:"Anxiety/Depression"}



        otp = output[single_prediction]
        print(otp, single_prediction)

        precautions = ['Seek professional help: If you\'re experiencing symptoms of depression, it\'s important to seek professional help. A mental health professional can help you understand your symptoms and develop a personalized treatment plan.', 'Stay connected: Social isolation can contribute to depression. Stay connected with family and friends and participate in social activities that you enjoy.', 'Practice self-care: Taking care of yourself physically and emotionally can help prevent or manage depression. Get regular exercise, eat a balanced diet, get enough sleep, and practice relaxation techniques, such as yoga or meditation.', 'Manage stress: Chronic stress can contribute to depression. Identify sources of stress in your life and develop strategies to manage them, such as time management, problem-solving, or seeking support from a therapist or support group.']

        diets = ['Focus on whole foods: A diet rich in whole foods, including fruits, vegetables, whole grains, lean proteins, and healthy fats, can provide the necessary nutrients for brain function and mood regulation.', 'Include omega-3 fatty acids: Omega-3 fatty acids, found in fatty fish, nuts, and seeds, may help reduce inflammation in the brain and improve symptoms of depression.', 'Limit processed and sugary foods: Processed and sugary foods may contribute to inflammation in the body, which has been linked to an increased risk of depression. Limit intake of processed and sugary foods and drinks.', 'Stay hydrated: Dehydration can cause fatigue and mood changes. Make sure to drink plenty of water and other hydrating fluids throughout the day.']

        return redirect('/predict8')

@app.route('/logout')
def logout():
    global login_status
    global uname
    login_status = ''
    uname = ''
    session.pop('email', None)
    return redirect('/')

if __name__ == '__main__':
    # sess.init_app(app)
    app.debug = True
    app.run()