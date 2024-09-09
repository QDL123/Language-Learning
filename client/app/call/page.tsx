'use client'

import { useState } from 'react';
import { redirect, useSearchParams } from "next/navigation";

import { motion } from 'framer-motion';
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

const tileVariants = {
  expanded: {
    width: 'var(--tile-expanded-width)',
    height: '90vh',
    transition: {
      duration: 0.5,
      ease: 'easeInOut',
    },
  },
  condensed: {
    width: 'var(--tile-condensed-width)',
    height: '60vh',
    transition: {
      duration: 0.5,
      ease: 'easeInOut',
    },
  },
};

const descriptionVariants = {
  visible: { opacity: 1, y: 0 },
  initial: { opacity: 0, y: -75 },
  hidden: { opacity: 0, y: -25 }
};

const retellWebClient = new RetellWebClient();

export default function Page() {
  // Configure call init animation.
  const [isExpanded, setIsExpanded] = useState(false);
  const [hidden, setHidden] = useState(false);
  const [callInProgress, setCallState] = useState(false);

  // Read in scenario details.
  const searchParams = useSearchParams()
  const scenario = searchParams.get('scenario');
  if (!scenario || !SCENARIOS.has(scenario)) {
    redirect('/scenarios');
  }
  const cardTitle = `SCENARIO: ${scenario}`.toUpperCase();
  const scenarioData = SCENARIOS.get(scenario)!;

  // Construct Retell calls.
  const handleCall = async () => {
    if (callInProgress) {
      console.log('Stopping call...');
      retellWebClient.stopCall();
    } else {
      console.log('Starting call...');
      fetch("http://127.0.0.1:8000/debug/start-call", {method: "POST"})
      .then((response) => response.json())
      .then((data) => {
        console.log(data);
        retellWebClient.startCall({
          accessToken: data.access_token,
        });
      })
      .catch(console.error);
    }
  }

  retellWebClient.on("call_started", () => {
    console.log("call started");
    setIsExpanded(true);
    setHidden(true);
    setCallState(true);
  });

  // TODO: trigger end-of-call flow.
  retellWebClient.on("call_ended", () => {
    console.log("call ended");
    setIsExpanded(false);
    setHidden(false);
    setCallState(false);
  });

  retellWebClient.on("update", (update) => {
    console.log(update);
  });

  retellWebClient.on("error", (error) => {
    console.error("An error occurred:", error);
  });

  return (
    <div className={styles.page}>
      <motion.div
      initial="condensed"
      animate={isExpanded ? 'expanded' : 'condensed'}
      variants={tileVariants}
      className={styles.tile}
    >
      <h2>{cardTitle}</h2>
      <motion.div
      initial="visible"
      animate={hidden ? "hidden" : "visible"}
      variants={descriptionVariants}
      transition={{ ease: [0.1, 0.25, 0.3, 1], duration: 0.6 }}
      className={styles.content}>
        <motion.div className={styles.description}>
          <p>{scenarioData.description}</p>
          <ol>
            {scenarioData.actionItems.map((item, index) => (
              <li key={index}>{item}</li>
            ))}
          </ol>
        </motion.div>
      </motion.div>

      <motion.div className={styles.footer}>
        <motion.div className={callInProgress ? styles.talkingWave : styles.hidden}>
            ...wave...
        </motion.div>
        <motion.div className={callInProgress ? styles.endbutton : styles.callbutton} onClick={handleCall}>
          {callInProgress ? 'End' : 'Start call'}
        </motion.div>
      </motion.div>
    </motion.div>
    </div>
  );
}
