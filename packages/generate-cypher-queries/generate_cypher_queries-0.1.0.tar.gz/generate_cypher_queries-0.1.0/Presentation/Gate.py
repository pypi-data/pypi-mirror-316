import time
from Logger import Logger
from Service import Service
class Gate:
    """
    This class provides an interface to generate query based on user input.
    """


    def __init__(self,uri="bolt://localhost:7687",user="neo4j",password="qwerty"):
        """
        This is the constructor for the Gate class. It initializes the service object and the Logger object.
        The default connection parameters are provided for connecting to a Neo4j database.
        :param uri:(str) The URI for the Neo4j database
        :param user: (str) The username for authentication
        :param password:(str) The password for authentication
        """
        self.service = Service(uri,user,password)
        self.logger = Logger().get_logger()

    def query(self,params):
        """
        This method processes a query depending on the provided params.
        it logs the time taken for the query execution.
        :param params: (list) A list of parameters that dictate the type of query (according to the standard)
        :return: The result of the query, in format of list fill with containing objects of type Record of Neo4j
        in case of an error returns None
        """
        if not self.input_validation(params):
            self.logger.error(f"unsupported input format")
            raise Exception("not supported input format")
        dict = {}
        results = None
        # in case of scheme query
        if len(params)==1:
            dict[f"{params[0]}"] = True
            dict["name"] = params[0]
            if params[0]=="edges":
                results = self.service.get_relations(dict)
            else:
                results = self.service.get_nodes_labels(dict)
            self.service.extract_CSV(dict)
            return results
        #fill the dictionary with the user requisites
        else:
            dict["startNode"] = params[0]
            lstofrelatedlabels = []
            if params[1]:
                lstofrelatedlabels.append(params[1])
                dict["relatedlabels"] = lstofrelatedlabels
            else:
                dict["relatedlabels"]= lstofrelatedlabels
            dict["source_columns"] = params[2]
            dict["target_columns"] = params[3]
            dict["flag_full_path"] = params[4]
            dict["name"] = params[5]
            if params[1] is not None:
                dict["asapath"] = "y"
            else:
                dict["asapath"] = "n"

            dict['limit'] = 10000
            dict['numberoflayers'] = 100

            start_time = time.time()
            results = self.service.get_by_param(dict)
            end_time = time.time()
            elapsed_time = end_time - start_time
            self.logger.info(f"this query last {elapsed_time} seconds")
            self.service.extract_CSV(dict)
            return results

    def input_validation(self,input):
        """
         Validates the structure of the input list based on predefined rules.
        This method checks that the input is a list with the correct number of elements and data types.
        :param input:  A list of elements that needs to be validated.
        :return:- `True` if the input is valid according to the criteria.
                - `False` if any validation step fails.
                In case of failure, detailed debug logs are provided.
        """
        if not isinstance(input, list):
            self.logger.debug(f"unsupported format, the input should be a list")
            return False

        if not isinstance(input[0], str):
            self.logger.debug(f"unsupported format, the first element in the list should contain string")
            return False

        if len(input)==1:
            if not (input[0] =="edges" or input[0] =="nodes"):
                self.logger.debug(f"unsupported format, the first element in the list should be edges or nodes based on needs")
                return False
        else:
            if len(input)!=6:
                self.logger.debug(f"unsupported format, the input must contain 6 items only")
                return False
            if not (isinstance(input[1], str) or input[1] is None):
                self.logger.debug(f"unsupported format, the second element in the list should be a string or None")
                return False
            if not isinstance(input[2], list):
                self.logger.debug(f"unsupported format, the third element in the list should be a list")
                return False
            for st in input[2]:
                if not (isinstance(st, str)):
                    self.logger.debug(f"unsupported format, each item in the third element in list should be a string")
                    return False
            if not isinstance(input[3], list):
                self.logger.debug(f"unsupported format, the forth element in the list should be a list")
                return False
            for st in input[3]:
                if not (isinstance(st, str)):
                    self.logger.debug(f"unsupported format, each item in the forth element in list should be a string")
                    return False
            if not isinstance(input[4],bool):
                self.logger.debug(f"unsupported format, the fifth element in input list should be a boolean flag")
                return False
            if not isinstance(input[5],str):
                self.logger.debug(f"unsupported format, the sixth element in input list should be a string")
                return False
            self.logger.debug(f"input validation is completed successfully")
            return True

