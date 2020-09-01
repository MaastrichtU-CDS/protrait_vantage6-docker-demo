import unittest
import vantage6.client as v6
import time
import logging

class TestStringMethods(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        logging.basicConfig(filename='logging.log',level=logging.INFO)
        self.__apiUrl = "http://localhost"
        self.__port = 5000
        self.__apiPath = "/api"
        self.__username = "johan"
        self.__password = "1234"
    
    # @classmethod
    # def tearDownClass(cls):
    #     cls._connection.destroy()

    def test_login(self):
        client = v6.Client(self.__apiUrl, self.__port, self.__apiPath)
        client.authenticate(self.__username, self.__password)

        client.setup_encryption(None)
        self.assertEqual(client.name, "Johan")

    def __summaryEqualToPredicted(self, outputStruct):
        expectedOutput = {'column_names_correct': True,
            'number_of_rows': 20,
            'ID': {
                'min': 1,
                'max': 20,
                'nan': 0,
                'mean': 10.5,
                'std': 2.946898458772509,
                'median': [7.627718676730986, 13.372281323269014]
                },
            'Age': {
                'min': 56,
                'max': 84,
                'nan': 0,
                'mean': 73.2,
                'std': 7.064365729341505,
                'median': [66.3145080059592, 80.08549199404081]
                },
            'Survival.Time.Days': {
                'min': 77,
                'max': 2165,
                'nan': 0,
                'mean': 608.0,
                'std': 715.9767785119997,
                'median': [77, 1305.8478415815298]
                },
            'deadstatus.event': {
                'min': 0,
                'max': 1,
                'nan': 0,
                'mean': 0.9,
                'std': 0.30779350562554625,
                'median': [0.6000000000000001, 1]
                }
            }
        self.assertEqual(expectedOutput, outputStruct)
    
    def test_summary(self):
        logging.info("Attempt login to Vantage6 API")
        client = v6.Client(self.__apiUrl, self.__port, self.__apiPath)
        client.authenticate(self.__username, self.__password)

        client.setup_encryption(None)

        input_ = {
            "master": "true",
            "method":"master", 
            "args": [
                {
                    "ID":"Int64",
                    "Age":"Int64", 
                    "Clinical.T.Stage":"category", 
                    "Clinical.N.Stage":"category",
                    "Clinical.M.Stage": "category",
                    "Overall.Ajcc.Stage": "category",
                    "Histology": "category",
                    "Sex": "category",
                    "Survival.Time.Days": "Int64",
                    "deadstatus.event": "Int64"}, 
                ".",
                ";"], 
            "kwargs": {}
        }

        logging.info("Requesting to execute summary algorithm")
        task = client.post_task(
            name="testing",
            image="harbor.vantage6.ai/algorithms/summary",
            collaboration_id=1,
            input_= input_,
            organization_ids=[1, 2]
        )

        logging.info("Wait and fetch results")
        res = client.get_results(task_id=task.get("id"))
        attempts=1
        while((res[0]["result"] == None) and attempts < 7):
            logging.info("waiting...")
            time.sleep(5)
            res = client.get_results(task_id=task.get("id"))
            attempts += 1
        self.__summaryEqualToPredicted(res[0]["result"])

if __name__ == '__main__':
    log_file = 'testResult.txt'
    with open(log_file, "w") as f:
        runner = unittest.TextTestRunner(f)
        unittest.main(testRunner=runner)