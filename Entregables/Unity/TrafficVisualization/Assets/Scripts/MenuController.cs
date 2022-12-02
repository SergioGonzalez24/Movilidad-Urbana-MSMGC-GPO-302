using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;

public class MenuController : MonoBehaviour
{
    /// Loads a scene based on the levelID parameter
    /// <param name="levelID">The ID of the level you want to load.</param>
    public void LoadGameLevel(int levelID)
    {
        SceneManager.LoadScene(levelID);
    }

    /// This function will exit the game
    public void ExitGame()
    {
        Application.Quit();
    }
}