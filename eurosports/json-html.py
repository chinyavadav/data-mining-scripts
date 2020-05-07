import csv
import ast
import json

template = """<section class='performance-facts' style='font-size:12px;border: 1px solid black;margin: 20px;float: left;width: 280px;padding: 0.5rem;'> <header class='performance-facts__header' style='border-bottom: 10px solid black;padding: 0 0 0.25rem 0;margin: 0 0 0.5rem 0;'> <h2 class='performance-facts__title' style='font-weight: bold;font-size: 1.3rem;margin: 0 0 0.25rem 0;'> Nutrition Facts</h2> <p style='margin: 0;'>Serving Size: {} </p> <p style='margin: 0;'>Serving Per Container: {}</p> </header> <table class='performance-facts__table' style='font-size:12px;width: 100%;border-collapse: collapse;'> <thead> <tr> <th colspan='3' class='small-info' style='font-size: 0.7rem;font-weight: normal;text-align: left;padding: 0.25rem 0;border-top: 1px solid black;white-space: nowrap;border: 0;'> Amount Per Serving </th> </tr> </thead> <tbody> {} </tbody> </table> <hr style='overflow: visible;box-sizing: content-box;height: 0;'> {} <hr style='overflow: visible;box-sizing: content-box;height: 0;'> <p class='small-info' style='margin: 0;font-size: 0.7rem;'><b>Ingredients:</b> {}</p> </section>"""

nutrient_bold_template = """ <tr> <th colspan='2' style='font-weight: normal;text-align: left;padding: 0.25rem 0;border-top: 1px solid black;white-space: nowrap;'><b style='font-weight: bolder;'>{}</b> {}</th> <td style="font-weight: normal;text-align: right;padding: 0.25rem 0;border-top: 1px solid black;white-space: nowrap;"><b style='font-weight: bolder;'>{}</b></td> </tr>"""
nutrient_template = """ <tr> <td class='blank-cell' style='font-weight: normal;text-align: left;padding: 0.25rem 0;border-top: 0;white-space: nowrap;width: 1rem;'> </td> <th style='font-weight: normal;text-align: left;padding: 0.25rem 0;border-top: 1px solid black;white-space: nowrap;'>{} {}</th> <td style='font-weight: normal;text-align: right;padding: 0.25rem 0;border-top: 1px solid black;white-space: nowrap;'><b style='font-weight: bolder;'>{}</b></td> </tr>"""

trail = """ <tr class='thick-row' style='font-size: 0.7rem;font-weight: normal;text-align: right;padding: 0.25rem 0;border-top: 1px solid black;white-space: nowrap;border-top-width: 5px;'> <td colspan='3' class='small-info'><b style='font-weight: bolder;'>% Daily Value*</b></td> </tr>"""

with open('nutrition.csv', 'r', encoding='utf-8', newline='') as csvfile:
    reader = csv.DictReader(csvfile)

    with open('nutrititon_html.csv', 'w', encoding='utf-8', newline='') as csvfile:
        fieldnames = ['ID', 'Short Description']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            ID = row['ID']
            Ingredients = row['Ingredients']
            BlendSet = ""
            if (row['Blends']) != "":
                Blends = ast.literal_eval(row['Blends'])
                for Blend in Blends:
                    temp = """<div style='font-size:12px;'><span>{}</span> <p class='small-info' style='margin: 0;font-size: 0.7rem;'>{}</p> </div>""".format(
                        Blend['name'], Blend['details'])
                    BlendSet = BlendSet + temp
            templateData = ""
            if (row['Nutrition'] != ""):
                Nutrition = ast.literal_eval(row['Nutrition'])
                lines = ""
                if (len(Nutrition) != 0):
                    for i in range(0, len(Nutrition[0]["NUTRIENTS"])):
                        nutrient = Nutrition[0]["NUTRIENTS"][i]
                        if nutrient['BOLDSTYLE'] == 1:
                            row_template = nutrient_bold_template
                        else:
                            row_template = nutrient_template
                        line = row_template.format(nutrient["NAME"],
                                                   nutrient["QUANTITY"], nutrient["DVPERCENT"])
                        if i == 0:
                            line = line+trail
                        lines = lines + line
                    templateData = template.format(
                        Nutrition[0]["SERVINGSIZEUOM"], Nutrition[0]["SERVINGSPERCONTAINER"], lines, BlendSet, Ingredients)
                else:
                    templateData = template.format(
                        "", "", "", BlendSet, Ingredients)
            else:
                templateData = template.format(
                    "", "", "", BlendSet, Ingredients)
            writer.writerow(
                {'ID': ID, 'Short Description': templateData.strip("\n")})
