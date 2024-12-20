"""
The runner can call the LLM in a loop and manage the stack of messages and functions
Research: we should understand the entropy at each stage and the overall resolution graph in the decision tree
"""

from pyaida.core.data import AbstractModel
from pyaida.core.lang.models import language_model_client_from_context, LanguageModel, CallingContext
from pyaida.core.lang.FunctionManager import FunctionManager
from pyaida.core.utils import logger, now
import json 
import typing
import traceback
from pyaida.core.lang.functions import FunctionCall, Function
from pyaida.core.lang.messages import MessageStack

class Runner:
    """Runners are simple objects that provide the interface between types and language models
    The message setup is the only function that plays with natural language.
    While almost all of the "prompting" is pushed out to types and functions,
    This setup function is the one function you can play with to make sure the comms are right with the LLM.
    For example it is here we inject plans (system prompt) and questions and other hints for how to run things.
    But by design, the critical guidance should be abstracted by Types and Functions.
    Beyond this, the rest is routine;
    - import type metadata and functions from the model which controls most everything
    - run an executor loop sending context to the LLM
    - implement the invocation and message setup methods to manage the function and message stack
    Under the hood the function manager handles actual function loading and searching
    """

    def __init__(self, model: AbstractModel = None, allow_help:bool=True):
        """
        A model is passed in or the default is used
        The reason why this is passed in is to supply a minimal set of functions
        If the model has no functions simple Q&A can still be exchanged with LLMs.
        More generally the model can provide a structured response format.
        """
        from pyaida import pg
        self.model: AbstractModel = model or None # DefaultAgentCore()
        self._function_manager = FunctionManager()
        self._allow_help = allow_help
        self.repo = pg.repository(self.model)
        self.initialize()
        
    def __repr__(self):
        return f"Runner({(self.model._get_name())})"

    def initialize(self):
        """register the functions and other metadata from the model"""
        self._context = None
        if self._allow_help:
            self._function_manager.add_function(self.help) # :)
        
        """register the model's functions which can include function search"""
        self._function_manager.register(self.model)
        """the basic bootstrapping means asking for help, entities(types) or functions"""
        self._function_manager.add_function(self.lookup_entity)
        self._function_manager.add_function(self.run_search)
        self._function_manager.add_function(self.activate_functions_by_name)
        """more complex things will happen from here when we traverse what comes back"""
        
        """whether we should put this crud here remains to be seen - it could be a property of the model instead"""
        #self._function_manager.add_function(self.save_entity)
    
    def run_search(self, questions: typing.List[str]):
        """run a search on the model that is being used in the current context as per the system prompt
        If you want to add multiple questions supply a list of strings as an array.
        Args:
            questions: ask one or more questions to search the data store
        """    
 
        return self.repo.run_search(questions)
    
    def activate_functions_by_name(self, function_names: typing.List[str], **kwargs):
        """
        provide a list of function names to load.
        The names should be fully qualified object_id.function_name
        """
        
 
        logger.debug(f'activating function {function_names}')
        fm = self._function_manager.add_functions_by_key(function_names)
        """todo check status"""
        return {
            'status': f"Re: the functions {function_names}, now ready for use. please go ahead and invoke."
        }
        
    def lookup_entity(self, name:str):
        """lookup entity by one or more keys. For example if you encounter entity names or keys in question, data etc you can use
        the entity search to learn more about them
        
        Args:
            name: one or more names to use to lookup the entity or entities 
        """
           
        logger.debug(f"lookup entity/{name=}")
       
        """todo test different parameter inputs e.g. comma separated"""
        entities =  self.repo(self.model).get_nodes_by_name(name,default_model=self.model)
        
        """register entity functions if needed and wait for the agent to ask to activate them"""
        for e in entities:
            self._function_manager.register(e)
        
        """when we return the entities, its better to return them with metadata (as opposed to just fetching the record data only)"""
        return AbstractModel.describe_models(entities)
    
    # def save_entity(self, entity:dict=None, structure_name: str=None, **kwargs):
    #     """Save entities that match the response schema given
        
    #     Args:
    #         entity: dictionary values matching the entity structure
    #         structure_name: if multiple known structures, provide the name
    #     """
        
    #     if not entity:
    #         """invariance to calling styles"""
    #         entity = kwargs
            
    #     try:
    #         _ =   self.repo.update_records(self.model(**entity))
    #         return {'status': 'entity save'}
    #     except Exception as ex: 
    #         return {'status': 'error', 'detail': repr(ex)}

    def help(self, questions: str | typing.List[str], context: str = None ):
        """if you are stuck ask for help with very detailed questions to help the planner find resources for you.
        If you have a hint about what the source or tool to use hint that in each question that you ask.
        For example, you can either just ask a question or you can ask "according to resource X" and then ask the question. This is important context.

        Args:
            questions (str): provide detailed questions to guide the planner. you should augment the users question with the additional context that you have e.g. a known source
            context: any added context e.g. what tool, function, source the user or system suggests may know the answer 
        """

        try:
            if context:
                questions = f"Using information from {context}, {questions}"
                
            """for now strict planning is off"""
            plan = self._function_manager.plan(questions,strict=False)
        except:
            return {"message": "planning pending - i suggest you use world knowledge"}

        """describe the plan context e.g. its a plan but you need to request the functions and do the thing -> update message stack"""

        return plan

    def invoke(self, function_call: FunctionCall):
        """Invoke function(s) and parse results into messages

        Args:
            function_call (FunctionCall): the payload send from an LLM to call a function
        """
        
        logger.debug(f"{function_call=}")
        
        f = self._function_manager[function_call.name]
        
        if not f:
            message = f"attempting to load function {function_call.name} which is not activated - please activate it"
            data = MessageStack.format_function_response_error(
                function_call.name, ValueError(message), self._context
            )
        else:

            try:
                """try call the function - assumes its some sort of json thing that comes back"""
                data = f(**function_call.arguments) or {}
                data = MessageStack.format_function_response_data(
                    function_call.name, data, self._context
                )
                """if there is an error, how you format the message matters - some generic ones are added
                its important to make sure the format coincides with the language model being used in context
                """
            except TypeError as tex: #type errors are usually the agents fault
                logger.warning(f"Error calling function {tex}")
                data = MessageStack.format_function_response_type_error(
                    function_call.name, tex, self._context
                )
            except Exception as ex: #general errors are usually our fault
                logger.warning(f"Error calling function {traceback.format_exc()}")
                data = MessageStack.format_function_response_error(
                    function_call.name, ex, self._context
                )

        #print(data) # maybe trace here
        """update messages with data if we can or add error messages to notify the language model"""
        self.messages.add(data)

    @property
    def functions(self) -> typing.Dict[str, Function]:
        """provide access to the function manager's functions"""
        return self._function_manager.functions

    def run(self, question: str, context: CallingContext=None, limit: int = None):
        """Ask a question to kick of the agent loop"""

        """setup all the bits before running the loop"""
        context = context or CallingContext()
        lm_client: LanguageModel = language_model_client_from_context(context)
        self._context = context
        
        self.messages = MessageStack(
            model=self.model,
            function_names=self.functions.keys(),
            language_model_provider=lm_client.get_provider())\
                .add_question(question)
             
        """run the agent loop to completion"""
        for _ in range(limit or context.max_iterations):
            response = None
            response = lm_client(
                messages=self.messages,
                context=context,
                functions=list(self.functions.values()),
            )
            if isinstance(response, FunctionCall):
                """call one or more functions and update messages"""
                self.invoke(response)
                continue
            if response is not None:
                # marks the fact that we have unfinished business
                break

        """fire telemetry"""

        """log questions to store unless disabled"""
        self.dump(question, response, context)
        
        """call the observer - often a no-op"""
        response = self.observe_structure(response)

        return response
    
    def observe_structure(self, response):
        """
        Particularly when the response is structured, if the user is not a system user, we may want to call the entity explainer
        - response = self.model.explain(response, explain_json_only=true)
        
        We may want to go the other way to when answers are unstructured to structure (and save) but that is probably already built in to the type behaviour
        - we describe types as "extractive" in that we can take unstructured data and structure and save it as a core type capability
        
        structured <--> unstructured decision making
        """
        return response

    def dump(self, questions: str, response: str, context: CallingContext):
        """dumps the messages and context to stores
        if the session is a typed objective this is updated in a slowly changing dimension
        generally audit all transactions unless disabled
        """
        from uuid import uuid4

        default_id = str(uuid4())

        """for any pydantic response"""
        if hasattr(response, "model_dump_json"):
            """dumpy state"""
            response = response.model_dump_json()

        try:
            # entity_store(ConversationModel).update_records(
            #     ConversationModel(
            #         id=default_id,
            #         user_id=context.username or "system",
            #         objective_node_id=context.session_id,
            #         content={"question": questions, "response": response},
            #     )
            # )
            pass
        except:
            print("Failure mode on dump TBD")
            pass


    def __call__(
        self, question: str, context: CallingContext = None, limit: int = None
    ):
        """
        Ask a question to kick of the agent loop
        """
        context = context or CallingContext()
        return self.run(question, context, limit=limit)

    def explain(cls, data:dict|typing.List[dict]):
        """
        it is often convenient to run the runner directly on data which uses this standard recipe
        """
        P = f"please explain the following data according to your guidelines - ```{json.dumps(data)}``` and respond in a json format - use the model provided"
        return cls(P)
    