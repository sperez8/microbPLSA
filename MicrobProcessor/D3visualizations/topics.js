
//the data
var topics = [
             {name: "Asparagus", type:0, protein: 2.2, calcium: 0.024, sodium: 0.002},
             {name: "Butter", type:0, protein: 0.85, calcium: 0.024, sodium: 0.714},
             {name: "Coffeecake", type:2, protein: 6.8, calcium: 0.054, sodium: 0.351},
             {name: "Pork", type:3, protein: 28.5, calcium: 0.016, sodium: 0.056},
             {name: "Provolone", type:1, protein: 25.58, calcium: 0.756, sodium: 0.876}
           ];
//decide which dimensions to show as axis
// and in what order
var dim = ['protein', 'sodium', 'calcium'];

//describe the type of each dimension (numerical or categorical/binary)
var types = {
		  "name": "string",
		  "type": "number",
		  "protein": "number",
		  "calcium": "number",
		  "sodium": "number",
		  "cake":"number"
		};