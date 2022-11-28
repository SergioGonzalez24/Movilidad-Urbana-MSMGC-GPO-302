// TC2008B. Sistemas Multiagentes y Gráficas Computacionales
// C# client to interact with Python. Based on the code provided by Sergio Ruiz.
// Octavio Navarro. October 2021


using System;
using System.Collections;
using System.Collections.Generic;
using UnityEditor;
using UnityEngine;
using UnityEngine.Networking;

public class CarData {
    public List<Vector4> positions;
}

public class Semaforos
{
    public List<Vector3> positions;
    public List<bool> states;
}

public class RunHandler
{
    public string message;
}
[Serializable]
public class TLightData
{
    public string id;
    public float x, y, z;
    public bool state;

    public TLightData(string id, float x, float y, float z, bool state)
    {
        this.id = id;
        this.x = x;
        this.y = y;
        this.z = z;
        this.state = state;
    }
}

[Serializable]
public class TLightsData
{
    public List<TLightData> positions;

    public TLightsData() => this.positions = new List<TLightData>();
}


public class Controller : MonoBehaviour
{
    string serverUrl = "localhost:8000";
    string getCarsEndpoint = "/getCars";
    string sendConfigEndpoint = "/init";
    string updateEndpoint = "/update";
    string getSemaforoEndpoint = "/getSemaforos";
    bool tlightStarted = false;
    TLightsData tlightsData;
    [SerializeField] string trafficEP;
    [SerializeField] GameObject semPrefab;
     Dictionary<string, GameObject> lights;
    Semaforos semaforos;
    GameObject[] semaforoList;
    public GameObject semaforo;
    CarData carsData;
    List<GameObject> cars;
    List<Vector3> oldPositions;
    List<Vector3> newPositions;
    
    // Pause the simulation while we get the update from the server
    bool hold = false;
    int currStep = 1, currLight = 0;
    float timer = 0.0f, dt = 0.0f;

    public GameObject carPrefab;
    public int carsNumber, lightSpan, maxSteps;
    public float timeToUpdate = 1.0f;

    void Start()
    {
        carsData = new CarData();
        oldPositions = new List<Vector3>();
        newPositions = new List<Vector3>();
        cars = new List<GameObject>();
        semaforoList = new GameObject[24];
        for (int i = 0; i < 24; i++)
        {
            semaforoList[i] = Instantiate(semPrefab, Vector3.zero, Quaternion.identity);
        }

        timer = timeToUpdate;

        for (int i = 0; i < carsNumber; i++)
            cars.Add(Instantiate(carPrefab, Vector3.zero, Quaternion.Euler(0, 180, 0)));

        StartCoroutine(SendConfiguration());
    }

    private void Update()
    {
        if (currStep <= maxSteps || maxSteps == -1)
        {
            float t = timer / timeToUpdate;
            // Smooth out the transition at start and end
            dt = t * t * (3f - 2f * t);

            if (timer >= timeToUpdate)
            {
                timer = 0;
                hold = true;
                StartCoroutine(UpdateSimulation());
            }

            if (!hold)
            {
                for (int s = 0; s < cars.Count; s++)
                {
                    Vector3 interpolated = Vector3.Lerp(oldPositions[s], newPositions[s], dt);
                    cars[s].transform.localPosition = interpolated;
                    Vector3 dir = oldPositions[s] - newPositions[s];
                    cars[s].transform.rotation = Quaternion.LookRotation(-dir);
                }
                // Move time from the last frame
                timer += Time.deltaTime;
            }
        }
    }

    IEnumerator SendConfiguration()
    {
        WWWForm form = new WWWForm();

        form.AddField("carsNumber", carsNumber.ToString());
        form.AddField("lightSpan", lightSpan.ToString());

        UnityWebRequest www = UnityWebRequest.Post(serverUrl + sendConfigEndpoint, form);
        www.SetRequestHeader("Content-Type", "application/x-www-form-urlencoded");

        yield return www.SendWebRequest();

        if (www.result != UnityWebRequest.Result.Success)
        {
            Debug.Log(www.error);
        }
        else
        {
            Debug.Log("Configuration upload complete!");
            Debug.Log("Getting Agents positions");
            StartCoroutine(GetCarsData());
            StartCoroutine(GetLightsData());
        }
    }

    IEnumerator UpdateSimulation()
    {
        UnityWebRequest www = UnityWebRequest.Get(serverUrl + updateEndpoint);
        yield return www.SendWebRequest();

        if (www.result != UnityWebRequest.Result.Success)
            Debug.Log(www.error);
        else
        {
            StartCoroutine(GetCarsData());
            currStep++;
            if (currLight == lightSpan)
            {
                UpdateTrafficLights();
                currLight = 0;
            }
            else if (currLight == lightSpan - 1)
            {
                UpdateTrafficLights();
                StartCoroutine(GetLightsData());
            }
            currLight++;
        }
    }

    IEnumerator GetCarsData()
    {
        UnityWebRequest www = UnityWebRequest.Get(serverUrl + getCarsEndpoint);
        yield return www.SendWebRequest();

        if (www.result != UnityWebRequest.Result.Success)
            Debug.Log(www.error);
        else
        {
            carsData = JsonUtility.FromJson<CarData>(www.downloadHandler.text);

            // Store the old positions for each agent
            oldPositions = new List<Vector3>(newPositions);
            newPositions.Clear();

            for (int v = 0; v < carsData.positions.Count; v++)
            {
                newPositions.Add(new Vector3(carsData.positions[v][0], carsData.positions[v][1], carsData.positions[v][2]));
                if (v > cars.Count)
                {
                    cars.Add(Instantiate(carPrefab, new Vector3(carsData.positions[v][0], carsData.positions[v][1], carsData.positions[v][2]), Quaternion.identity));
                }

                // isStopped = (int) carsData.positions[v][3];
            }

            hold = false;
        }
    }
    IEnumerator GetLightsData(){
            UnityWebRequest www = UnityWebRequest.Get(serverUrl + getSemaforoEndpoint);
            yield return www.SendWebRequest();
            if (www.result != UnityWebRequest.Result.Success)
                Debug.Log(www.error);
            else{
                tlightsData = JsonUtility.FromJson<TLightsData>(www.downloadHandler.text);

                foreach(TLightData light in tlightsData.positions)
                {
                    // Instanciar semaforos
                    if (!tlightStarted)
                    {
                        Vector3 lightPosition = new Vector3(light.x, light.y, light.z);
                        lights[light.id] = Instantiate(semaforo, lightPosition, Quaternion.identity);
                        lights[light.id].name = light.id;
                    }
                    // Si el semaforo ya existe, modificar su estado
                    else
                    {
                        if(light.state){
                            lights[light.id].GetComponent<Light>().color = Color.green;
                        } else {
                            lights[light.id].GetComponent<Light>().color = Color.red;
                        }
                    }
                }
                if (!tlightStarted) tlightStarted = true;
            }
        }
    /*void updateTrafficLights() {
    	foreach(GameObject trafficLight in CityMaker.Instance.trafficLights) {
    		if(trafficLight.transform.GetChild(2).gameObject.activeInHierarchy && currLight == lightSpan-1) {
    			trafficLight.transform.transform.GetChild(2).gameObject.SetActive(false);
    			trafficLight.transform.transform.GetChild(0).gameObject.SetActive(false);
	    		trafficLight.transform.transform.GetChild(1).gameObject.SetActive(true);
    		} else if(trafficLight.transform.GetChild(1).gameObject.activeInHierarchy && currLight == lightSpan) {
    			trafficLight.transform.transform.GetChild(1).gameObject.SetActive(false);
    			trafficLight.transform.transform.GetChild(2).gameObject.SetActive(false);
	    		trafficLight.transform.transform.GetChild(0).gameObject.SetActive(true);
    		} else if(trafficLight.transform.GetChild(0).gameObject.activeInHierarchy && currLight == lightSpan) {
	    		trafficLight.transform.transform.GetChild(0).gameObject.SetActive(false);
    			trafficLight.transform.transform.GetChild(1).gameObject.SetActive(false);
    			trafficLight.transform.transform.GetChild(2).gameObject.SetActive(true);
    		}
    	}    
    }*/


    IEnumerator UpdateTrafficLights()
    {
        UnityWebRequest www = UnityWebRequest.Get(serverUrl + trafficEP);
        yield return www.SendWebRequest();

        if (www.result == UnityWebRequest.Result.Success)
        {
            //Debug.Log(www.downloadHandler.text);
            semaforos = JsonUtility.FromJson<Semaforos>(www.downloadHandler.text);
            MoveSem();

        }
        else
        {
            Debug.Log(www.error);
        }
    }

    void MoveSem()
    {
        for (int i = 0; i < 24; i++)
        {
            semaforoList[i].transform.position = semaforos.positions[i];
            semaforoList[i].GetComponent<LuzSemaforo>().toggleLight(semaforos.states[i]);
            Debug.Log(semaforos.states[i]);
        }

    }
}
