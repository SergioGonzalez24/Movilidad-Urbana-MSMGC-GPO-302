// TC2008B. Sistemas Multiagentes y Gráficas Computacionales
// C# client to interact with Python. Based on the code provided by Sergio Ruiz.
// Octavio Navarro. October 2021


using System;
using System.Collections;
using System.Collections.Generic;
using UnityEditor;
using UnityEngine;
using UnityEngine.Networking;

/* It's a list of Vector4s. */
public class DatosMcqueen {
    public List<Vector4> positions;
}

public class Controller : MonoBehaviour {
    /* The above code is setting up the variables that will be used in the program. */
    string serverUrl = "localhost:8000";
    string getCarsEndpoint = "/getMcqueen";
    string sendConfigEndpoint = "/init";
    string updateEndpoint = "/update";
    
    DatosMcqueen carsData;
    List<GameObject> cars;
    List<Vector3> prevPositions;
    List<Vector3> curPositions;
    bool hold = false;
    int currStep = 1, currLight = 0;
    float timer = 0.0f, dt = 0.0f;

    public GameObject carPrefab;
    public int obten_Mcqueen, tiempo, maxSteps;
    public float timeToUpdate = 1.0f;

    /// It creates a list of cars, and then starts a coroutine that sends the configuration to the server.
    void Start() {
        carsData = new DatosMcqueen();
        prevPositions = new List<Vector3>();
        curPositions = new List<Vector3>();

        cars = new List<GameObject>();

        timer = timeToUpdate;

        for(int i = 0; i < obten_Mcqueen; i++)
            cars.Add(Instantiate(carPrefab, Vector3.zero, Quaternion.Euler(0, 180, 0)));
            
        StartCoroutine(SendConfiguration());
    }
        /// If the current step is less than the maximum number of steps, or the maximum number of steps is -1
        /// (infinite), then we calculate the delta time, and if the timer is greater than the time to update,
        /// we start the coroutine to update the simulation. If the hold variable is false, we interpolate the
        /// positions of the cars, and set the rotation of the cars to look at the previous position. Finally,
        /// we increment the timer
    private void Update() 
    {
    	if(currStep <= maxSteps || maxSteps == -1) {
		    float t = timer/timeToUpdate;
		    dt = t * t * ( 3f - 2f*t);
		    if(timer >= timeToUpdate) {
		        timer = 0;
		        hold = true;
		        StartCoroutine(UpdateSimulation());
		    }

		    if (!hold) {
		        for (int s = 0; s < cars.Count; s++) {
		            Vector3 interpolated = Vector3.Lerp(prevPositions[s], curPositions[s], dt);
		            cars[s].transform.localPosition = interpolated;
		            
		            Vector3 dir = prevPositions[s] - curPositions[s];
		            cars[s].transform.rotation = Quaternion.LookRotation(-dir);
                    
		            
		        }
		        timer += Time.deltaTime;
		    }
        }
    }
 
    /// We create a new WWWForm object, add the values we want to send to the server, create a new
    /// UnityWebRequest object, set the request header, send the request, and then check if the request was
    /// successful
    IEnumerator SendConfiguration()
    {
        WWWForm form = new WWWForm();

        form.AddField("Mcqueens", obten_Mcqueen.ToString());
        form.AddField("tiempo", tiempo.ToString());

        UnityWebRequest www = UnityWebRequest.Post(serverUrl + sendConfigEndpoint, form);
        www.SetRequestHeader("Content-Type", "application/x-www-form-urlencoded");

        yield return www.SendWebRequest();

        if (www.result != UnityWebRequest.Result.Success)
        {
            Debug.Log(www.error);
        }
        else
        {
            StartCoroutine(ObtenMcqueens());
        }
    }

    /// It sends a request to the server to update the simulation, and then it calls the function that gets
    /// the new positions of the cars
	IEnumerator UpdateSimulation() {
        UnityWebRequest www = UnityWebRequest.Get(serverUrl + updateEndpoint);
        yield return www.SendWebRequest();
 
        if (www.result != UnityWebRequest.Result.Success)
            Debug.Log(www.error);
        else {
            StartCoroutine(ObtenMcqueens());
	        currStep++;
	        if(currLight == tiempo) {
	        	ActualizaLuces();
	        	currLight = 0;
	        } else if(currLight == tiempo-1) {
	        	ActualizaLuces();
	        }
	        currLight++;
        }
    }

    /// It gets the data from the server, parses it, and then updates the positions of the cars in the Unity
    /// scene
    IEnumerator ObtenMcqueens() {
        UnityWebRequest www = UnityWebRequest.Get(serverUrl + getCarsEndpoint);
        yield return www.SendWebRequest();
 
        if (www.result != UnityWebRequest.Result.Success)
            Debug.Log(www.error);
        else {
            carsData = JsonUtility.FromJson<DatosMcqueen>(www.downloadHandler.text);
            prevPositions = new List<Vector3>(curPositions);
            curPositions.Clear();

            for(int v = 0; v < carsData.positions.Count; v++) {
                curPositions.Add(new Vector3(carsData.positions[v][0], carsData.positions[v][1], carsData.positions[v][2]));
                if(v > cars.Count) {
                	cars.Add(Instantiate(carPrefab, new Vector3(carsData.positions[v][0], carsData.positions[v][1], carsData.positions[v][2]), Quaternion.identity));
                }
            }
            hold = false;
        }
    }
    
    /// If the current light is the last light, turn it off and turn on the first light. If the current
    /// light is the first light, turn it off and turn on the second light. If the current light is the
    /// second light, turn it off and turn on the third light
    void ActualizaLuces() {
    	foreach(GameObject luzsemaforo in CityMaker.Instance.Semaforo) {
    		if(luzsemaforo.transform.GetChild(2).gameObject.activeInHierarchy && currLight == tiempo-1) {
    			luzsemaforo.transform.transform.GetChild(2).gameObject.SetActive(false);
    			luzsemaforo.transform.transform.GetChild(0).gameObject.SetActive(false);
	    		luzsemaforo.transform.transform.GetChild(1).gameObject.SetActive(true);
    		} else if(luzsemaforo.transform.GetChild(1).gameObject.activeInHierarchy && currLight == tiempo) {
    			luzsemaforo.transform.transform.GetChild(1).gameObject.SetActive(false);
    			luzsemaforo.transform.transform.GetChild(2).gameObject.SetActive(false);
	    		luzsemaforo.transform.transform.GetChild(0).gameObject.SetActive(true);
    		} else if(luzsemaforo.transform.GetChild(0).gameObject.activeInHierarchy && currLight == tiempo) {
	    		luzsemaforo.transform.transform.GetChild(0).gameObject.SetActive(false);
    			luzsemaforo.transform.transform.GetChild(1).gameObject.SetActive(false);
    			luzsemaforo.transform.transform.GetChild(2).gameObject.SetActive(true);
    		}
    	}    
    }

}