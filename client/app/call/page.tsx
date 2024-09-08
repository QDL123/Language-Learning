'use client'

import { redirect, useSearchParams } from "next/navigation";

import { RetellWebClient } from "retell-client-js-sdk";

import styles from "./page.module.css";

interface ScenarioDetails {
  description: string,
  actionItems: string[]
};

// TODO: pull this from backend which tracks supported scenarios.
const SCENARIOS: Map<string, ScenarioDetails> = new Map([
  [
    'restaurant',
    {
      description: `You will speak with the hostess of a restaurant in Spanish to
                    make a reservation. Your tutor will be available if you need
                    to speak English.`,
      actionItems: [
        'Provide your name',
        'Ask if they have availabilty next Wednesday at 6pm',
        'Request a reservation for 6 people',
        'Tell them it\'s for a birthday'
      ]
    }
  ]
]);


export default function Page() {
  const searchParams = useSearchParams()
  const scenario = searchParams.get('scenario');
  if (!scenario || !SCENARIOS.has(scenario)) {
    redirect('/scenarios');
  }

  const cardTitle = `SCENARIO: ${scenario}`.toUpperCase();
  const scenarioData = SCENARIOS.get(scenario)!;

  const retellWebClient = new RetellWebClient();
  const initiateCall = async () => {
    console.log('Starting call...');
    await retellWebClient.startCall({
      accessToken: '',
    });
  };

  retellWebClient.on("call_started", () => {
    console.log("call started");
  });

  // TODO: trigger end-of-call flow.
  retellWebClient.on("call_ended", () => {
    console.log("call ended");
  });

  retellWebClient.on("error", (error) => {
    console.error("An error occurred:", error);
  });

  return (
    <div className={styles.page}>
      <div className={styles.tile}>
        <h2>{cardTitle}</h2>
        <p>{scenarioData.description}</p>
        <ol>
          {scenarioData.actionItems.map((item, index) => (
            <li key={index}>{item}</li>
          ))}
        </ol>
        <div className={styles.button} onClick={initiateCall}>
          Start call
        </div>
      </div>
    </div>
  );
}