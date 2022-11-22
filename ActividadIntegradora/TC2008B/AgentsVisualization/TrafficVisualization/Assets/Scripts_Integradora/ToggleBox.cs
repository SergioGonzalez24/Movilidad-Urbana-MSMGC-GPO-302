using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class ToggleBox : MonoBehaviour
{
    public GameObject Box;
    public Light Luz;
    
    // Start is called before the first frame update
    void Start()
    {
        Box.SetActive(false);
        Luz.color = Color.green;
    }

    public void RemoveBox()
    {
        Box.SetActive(false);
        Luz.color = Color.green;
    }

    public void AddBox()
    {
        Box.SetActive(true);
        Luz.color = Color.red;
    }
}
