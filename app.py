from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, redirect
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///patients.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    age = db.Column(db.Integer)
    height = db.Column(db.Float)
    weight = db.Column(db.Float)
    issues = db.Column(db.String(200))

diet_chart = {
    "Diabetes": {"foods": ["Brown rice", "Oats", "Bitter gourd", "Fenugreek"], "avoid": ["Sugar", "White rice", "Sweets"]},
    "PCOS": {"foods": ["Flax seeds", "Vegetables", "Fruits", "Moong dal"], "avoid": ["Junk food", "Cheese"]},
    "Thyroid": {"foods": ["Iodized salt", "Curd", "Apple"], "avoid": ["Soy", "Cabbage"]},
    "Obesity": {"foods": ["Millets", "Green tea", "Salads"], "avoid": ["Fried food", "Bakery items"]},
    "Anemia": {"foods": ["Spinach", "Beetroot", "Dates", "Jaggery"], "avoid": ["Tea after meals"]},
    "Hypertension": {"foods": ["Banana", "Garlic", "Oats"], "avoid": ["Salt", "Pickles"]},
    "Acidity": {"foods": ["Banana", "Buttermilk", "Coconut water"], "avoid": ["Spicy food", "Tea"]},
    "Constipation": {"foods": ["Papaya", "Warm water", "Ghee", "Oats"], "avoid": ["Processed food"]},
    "Hair fall": {"foods": ["Almonds", "Walnuts", "Spinach", "Carrot"], "avoid": ["Junk food"]},
    "Skin problems": {"foods": ["Neem", "Turmeric milk", "Cucumber"], "avoid": ["Fried food", "Sugar"]}
}

food_images = {
    "Brown rice":"brownrice.jpg","Oats":"oats.jpg","Bitter gourd":"bittergourd.jpg","Fenugreek":"fenugreek.jpg",
    "Flax seeds":"flaxseed.jpg","Vegetables":"veggies.jpg","Fruits":"fruits.jpg","Moong dal":"moongdal.jpg",
    "Iodized salt":"salt.jpg","Curd":"curd.jpg","Apple":"apple.jpg",
    "Millets":"millets.jpg","Green tea":"greentea.jpg","Salads":"salads.jpg",
    "Spinach":"spinach.jpg","Beetroot":"beetroot.jpg","Dates":"dates.jpg","Jaggery":"jaggery.jpg",
    "Banana":"banana.jpg","Garlic":"garlic.jpg",
    "Buttermilk":"buttermilk.jpg","Coconut water":"coconutwater.jpg",
    "Papaya":"papayaa.jpg","Warm water":"warmwater.jpg","Ghee":"ghee.jpg",
    "Almonds":"almonds.jpg","Walnuts":"walnuts.jpg","Carrot":"carrot.jpg",
    "Neem":"neem.jpg","Turmeric milk":"turmericmilk.jpg","Cucumber":"cucumber.jpg"
}

@app.route("/")
def home():
    issues = list(diet_chart.keys())
    return render_template("index.html", issues=issues)

@app.route("/form")
def form():
    issues = list(diet_chart.keys())
    return render_template("index.html", issues=issues)

@app.route("/result", methods=["POST"])
def result():
    name = request.form["name"]
    if not name.replace(" ", "").isalpha():
        return "Name should contain only letters"
    age = int(request.form["age"])
    height = float(request.form["height"])
    weight = float(request.form["weight"])
    if age <= 0 or age > 120:
        return "Enter valid age"
    if height < 50 or height > 250:
        return "Enter valid height"
    if weight < 10 or weight > 250:
        return "Enter valid weight"

    height_m = height / 100
    bmi = round(weight / (height_m ** 2), 2)
    if bmi < 18.5:
        bmi_status = "Underweight"
    elif bmi < 25:
        bmi_status = "Normal"
    else:
        bmi_status = "Overweight"

    selected_issues = request.form.getlist("issues")
    recommended = set(); avoid = set()
    for issue in selected_issues:
        recommended.update(diet_chart[issue]["foods"])
        avoid.update(diet_chart[issue]["avoid"])

    issues_str = ", ".join(selected_issues)
    new_patient = Patient(
        name=name,
        age=age,
        height=height,
        weight=weight,
        issues=issues_str
    )
    db.session.add(new_patient)
    db.session.commit()

    return render_template(
        "result.html",
        name=name,
        bmi=bmi,
        bmi_status=bmi_status,
        issues=selected_issues,
        foods=recommended,
        avoid=avoid,
        food_images=food_images
    )

@app.route("/patients")
def patients():
    all_patients = Patient.query.all()
    return render_template("patients.html", patients=all_patients)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)