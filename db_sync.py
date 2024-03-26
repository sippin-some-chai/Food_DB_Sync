import csv
import mysql.connector

recipe_name = ""
protien = 0
calories = 0
ingredients = []

user_input = input("Enter Recipe: ")
recipe_name = user_input
ingredient_count = 0
while True:
    ingredient_count+=1
    user_input = input(f"Ingredient [{ingredient_count}]: ")    
    if user_input.lower() == "f":
        print("Recipe is " + recipe_name)
        print("Ingredients are ")
        print(ingredients)
        user_input = input("Good? ")
        if user_input.lower() == "y":
            break
    ingredients.append(user_input)

print("###################Accessing Database##################")    
mydb = mysql.connector.connect(
    host="OPE",
    user="NICE TRY",
    password="HA",
    database="ECHOING!"
)

mycursor = mydb.cursor()
sql = ''
check_avail_rec =" SELECT * FROM Recipes WHERE name='" + recipe_name + "'"
mycursor.execute(check_avail_rec)
rec_result = mycursor.fetchone()

recipe_id = 0
ingredient_id = 0

if rec_result is None:
    print("Recipe Not Detected Adding...")
    user_input = input("Calories? ")
    calories = float(user_input)
    user_input = input("Protien? ")
    protien = float(user_input)
    user_input = input("Time to Cook? ")
    time = float(user_input);
    user_input = ("Type of Meal? ")
    meal_type = user_input
    user_input = input("Description? ")
    description = user_input 
    add_recipe = "INSERT INTO Recipes (name, description, calories, protien, time, type) VALUES (%s, %s, %s, %s, %s, %s)"
    mycursor.execute(add_recipe, (recipe_name, description, calories, protien, time, meal_type))
    mydb.commit()
    recipe_id = mycursor.lastrowid 
else:
    print(f"Found {recipe_name} in DB! ..checking ingredient consistency...")
    recipe_id = rec_result[0]
for j in range(0,len(ingredients)):
    ingredient = ingredients[j]
    unit = "hmmm"
    check_ingredient = " SELECT * FROM Ingredients WHERE name='"+ ingredient +"'"
    mycursor.execute(check_ingredient)
    ing_result = mycursor.fetchone()
    if ing_result is None:
        print(f"{ingredient} not found..adding to ingredient table")
        unit = input("Units found in? ")
        quantity = input(f"{unit} Available? ")
        expiration = input("Expiration(yyyy-mm-dd)? ")
        insert_ingred = "INSERT INTO Ingredients (name, unit, expiration, quantity) VALUES (%s, %s, %s, %s)"
        mycursor.execute(insert_ingred, (ingredient, unit, expiration, quantity))
        mydb.commit()
        ingredient_id = mycursor.lastrowid
    else:
        print(f"Found {ingredient}!")
        ingredient_id = ing_result[0]
        unit = ing_result[2]
    print("..checking mappings")
    search_mapping = ("SELECT * FROM Recipe_Junc WHERE ingredient_id = %s AND recipe_id = %s")
    mycursor.execute(search_mapping,(ingredient_id, recipe_id))
    junc_result = mycursor.fetchone()
    if (junc_result) is None:
        print(f"Creating mapping between {recipe_name} and {ingredient}")
        recipe_quant = float(input(f"Amount Required for Recipe(in {unit})? "))
        insert_mapping = "INSERT INTO Recipe_Junc (recipe_id, ingredient_id, quantity) VALUES (%s, %s, %s)"
        mycursor.execute(insert_mapping, (recipe_id, ingredient_id, recipe_quant))
        mydb.commit()
    else:
        print(f"found mapping for {ingredient} moving on...")
