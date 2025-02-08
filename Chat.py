import sqlalchemy
import ollama
import json
from time import sleep


class Company_Chatbot:
	def __init__(self):
		self.system_prompt = ""
		
		#Read System prompt from text file
		with open("system_prompt.txt","r") as f:
		    self.system_prompt = f.read()
		#Define the tool for fetching data from SQL
		SQL_tool = {
		    "name" : "SQLFetchTool",
		    "description" : "Accepts and executes a single SQL query. Returns all the sql rows in the form of list of tuples. Call this tool to execute your SQL query.",
		    "parameters" : {
		        "type" : "object",
		        "properties" : {
		            "Query" : {
		                "type" : "string",
		                "description" : "The functional query generated from the user query",
		            },  
		        },
		        "required" : ["Query"],
		        "additionalProperties" : False
		    }    
		}
		#Prepare the tool to pass into model respond function
		self.tool = [{"type" : "function", "function" : SQL_tool}]


	def SQLFetchTool(self,Query):
	    """
	    Execute SELECT queries on a SQLite database with enhanced error handling.
	    
	    Args:
	        Query (str): SQL query to execute
	        
	    Returns:
	        str: Query results or error message
	    """
	    # Input validation
	    if not Query or not isinstance(Query, str):
	        print("Error: Query must be a non-empty string")
	        return "Error: Query must be a non-empty string"
	    
	    # Check if query is empty after trimming whitespace
	    cleaned_query = Query.strip()
	    if not cleaned_query:
	        print("Error: Empty query")
	        return "Error: Empty query"

	    # Check for SELECT query
	    if not cleaned_query.split()[0].upper() == "SELECT":
	        print("Unauthorized Query: Only SELECT queries are allowed")
	        return "Error: You are not authorized to run non-SELECT queries"

	    try:
	        # Database connection
	        engine = sqlalchemy.create_engine('sqlite:///Company.db', echo=False)
	        print(f"Input Query: {Query}")

	        try:
	            with engine.connect() as connection:
	                # Query execution
	                try:
	                    results = connection.execute(sqlalchemy.text(Query))
	                    res = results.fetchall()
	                    
	                    # Handle empty results
	                    if not res:
	                        return "No results found"
	                    
	                    # Format results
	                    try:
	                        ans = ""
	                        for tple in res:
	                            #add all tuples to a single string
	                            ans += f"{tple}, "
	                        return ans.rstrip(", ")  # Remove trailing comma and space
	                    
	                    #Error Handling for formatting
	                    except Exception as e:
	                        print(f"Error formatting results: {str(e)}")
	                        return "Error: Failed to format query results"

	                #Error Handling for Query execution
	                except sqlalchemy.exc.SQLAlchemyError as e:
	                    print(f"Query execution error: {str(e)}")
	                    return f"Error executing query: {str(e)}"
	        
	        #Error Handling for connection fault
	        except sqlalchemy.exc.DatabaseError as e:
	            print(f"Database connection error: {str(e)}")
	            return "Error: Unable to connect to database"
	    
	    #Error Handling for engine fault (in case the database name is wrong)
	    except Exception as e:
	        print(f"Engine creation error: {str(e)}")
	        return "Error: Failed to initialize database connection"
	    
	    finally:
	        # Ensure engine is disposed
	        try:
	            engine.dispose()
	        except:
	            pass

	def tool_call_handling(self,tool_calls):
	    """
	    Handle tool calls and return the results with error handling
	    
	    Args:
	        tool_calls: List of tool call objects
	        
	    Returns:
	        list: List of dictionaries containing tool call results and metadata
	    """
	    try:
	        results = []
	        count = 0
	        result = ""
	 

	        for tool_call in tool_calls:
	            #get function name and arguements
	            function_name = tool_call.function.name
	            function_args = tool_call.function.arguments
	            
	            #Handle Function Call
	            if function_name == "SQLFetchTool":
	                #Logging for Tool Call and calling the tool
	                print("-----Tool Called-----")
	                result = self.SQLFetchTool(function_args["Query"])
	            
	            else:
	                #Incase the models decides to use invalid tool
	                result = f"Unknown function: {function_name}"

	            #Logging the results of the query
	            print(f"Query Result : {result}")

	            #Compile the result of all tool calls and return them in proper dictionary format
	            results.append({
	                "tool_call_index": count,
	                "function_name": function_name,
	                "result": result
	            })
	            #Use count as tool id because ollama api does not provide any
	            count +=1

	        return results

	    #Handle All Errors in this function (Very unlikely as this function is only accessed by the LLM)
	    except Exception as e:
	         print(f"Failed to process tool calls: {str(e)}")
	         return [{"tool_call_ind": count, "function_name" : function_name, "result" : "Error while trying to execute query"}]


	def chat_func(self,message,history = [],MODEL="llama3.2"):
	    """
	    Handle chat interactions with a model, including tool call processing.
	    
	    Args:
	        message (str): The user's message to the chat model.
	        history (list, optional): The conversation history. Defaults to an empty list.
	        MODEL (str, optional): The model to use for the chat. Defaults to "llama3.2".
	        
	    Yields:
	        str: Partial responses from the model.
	    """
	    try:
	        # Validate input
	        if message is None or message.strip() == "":
	            raise ValueError("Message cannot be None or empty")
	        #Just in case
	        if history is None:
	            history = []

	        # Construct model input
	        model_input = [{"role": "system", "content": self.system_prompt}] + history + [{"role": "user", "content": message}]

	        # Get initial response from the model
	        try:
	            response = ollama.chat(model=MODEL, messages=model_input, tools=self.tool)
	        except Exception as e:
	            raise Exception(f"Error during initial chat model call: {str(e)}")

	        # Handle tool calls if present
	        if response.message.tool_calls:
	            try:
	                #Tool call is handled by another class method
	                tool_results = self.tool_call_handling(response.message.tool_calls)
	                #Structure the tool results to pass into context window of the LLM
	                tool_messages = [
	                    {"role": "assistant", "content": None, "tool_calls": response.message.tool_calls},
	                    {"role": "tool", "content": json.dumps(tool_results)}
	                ]

	                # Get response after adding tool context into the context window
	                try:
	                    tool_response = ollama.chat(model=MODEL, messages=model_input + tool_messages, stream=True)
	                except Exception as e:
	                    #Raise exception in case of any errors
	                    raise Exception(f"Error during tool response chat model call: {str(e)}")

	                #Stream the results from the tool response
	                partial_response = ""
	                for chunk in tool_response:
	                    if not isinstance(chunk.message.content, tuple):
	                        partial_response += chunk.message.content
	                        yield partial_response

	            except Exception as e:
	                print(f"Error handling tool calls: {str(e)}")
	                yield "Unkown Exception Occured. Please report this to the Admin"

	        #Stream the results from the original response
	        partial_response = ""
	        for char in response.message.content:
	            if not isinstance(char, tuple):
	                sleep(0.05)
	                partial_response += char
	                yield partial_response

	    except Exception as e:
	        print(f"An error occurred: {str(e)}")
	        yield "Unkown Exception Occured. Please report this to the Admin"