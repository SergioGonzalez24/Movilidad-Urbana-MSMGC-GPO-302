using System.Collections;
using System.Collections.Generic;
using UnityEngine;




public class SemaforoLuz : MonoBehaviour
{
    [SerializeField] Light semLight;
    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        
    }

    public void toggleLight(bool state)
    {
        if(state)
            semLight.color = Color.green;
        else
            semLight.color = Color.red;
    }

}
