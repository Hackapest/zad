from spyre import server
from lab3 import loadFiles

df = loadFiles("vhi_data_15-03-2024_23-19-19")
print(df)

class SimpleApp(server.App):
	title = "Simple App"
	inputs = [{
		"type": "text",
		"key": "words",
		"label": "write words here",
		"value": "hello world", 
		"action_id": "simple_html_output"
	}]

    outputs = [
        {"type": "table", "id": "table", "control_id": "simple_html_output", "tab": "Таблиця"},
        {"type": "plot", "id": "plot", "control_id": "simple_html_output", "tab": "Графік"}
    ]

	def getHTML(self, params):
		words = params["words"]
		return df



app = SimpleApp()
app.launch()