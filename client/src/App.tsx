import { Button, Skeleton } from "@mui/material";
import KonfuzioLogo from "./assets/konfuzio-logo.svg";
import "./App.css";
import { useState } from "react";
import axios from "axios";

function App() {
  const [botNames, setBotNames] = useState<string[]>([]);
  const [botJokes, setBotJokes] = useState<string[]>([]);
  const [loading, setLoading] = useState<boolean>(false);

  const callComedians = async () => {
    setLoading(true);
    const response = await axios.get("http://localhost:8000/");
    const botNames = [];
    const jokesList = [];

    for (let botName in response.data) {
      if (response.data.hasOwnProperty(botName)) {
        botNames.push(botName);
        const joke = response.data[botName].replace(/\n/g, "").trim();
        console.log(joke);
        jokesList.push(joke);
      }
    }
    setBotNames(botNames);
    setBotJokes(jokesList);
    setLoading(false);
  };

  return (
    <>
      <a href="https://konfuzio.com/en/" target="_blank">
        <img src={KonfuzioLogo} alt="Konfuzio Logo" className="logo" />
      </a>
      <h2>
        Welcome to the AI-Comedy Club by{" "}
        <a href="https://konfuzio.com/en/" target="_blank">
          Konfuzio.ai
        </a>{" "}
        👋
      </h2>
      <div>
        <div>
          If you want to ask the Contenders to take the stage and give us their
          top jokes click on the following button:
        </div>
        <Button variant="contained" color="primary" onClick={callComedians}>
          {loading ? "Loading..." : "Call the Contenders"}
        </Button>
        {
          // If loading is true, display a loading skeleton
          loading ? (
            <div>
              <Skeleton height={100} />
              <Skeleton animation="wave" height={100} />
              <Skeleton animation={false} height={100} />
            </div>
          ) : (
            // If loading is false, display the jokes
            <div>
              {botNames.map((botName, index) => (
                <div key={botName} className="joke_item">
                  <h3 className="bot_title">{botName}:</h3>
                  <span className="bot_joke">{botJokes[index]}</span>
                </div>
              ))}
            </div>
          )
        }
      </div>
    </>
  );
}

export default App;
