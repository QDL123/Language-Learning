import styles from "./page.module.css";

export default function Home() {
  return (
    <div className={styles.page}>
      <main className={styles.main}>
        <h1 className={styles.title}>
          LANGUAGE LEARNING THROUGH CONVERSATION
        </h1>

        <div className={styles.buttons}>
          <a
            className={styles.primary}
            href="/call?scenario=restaurant"
            rel="noopener noreferrer"
          >
            Try Demo
          </a>
        </div>
      </main>
      <footer className={styles.footer}>
        <a
          href="https://cmaks.dev"
          target="_blank"
          rel="noopener noreferrer"
        >
          Clay Maksymiuk
        </a>
         · 
        <a
          href="https://github.com/QDL123"
          target="_blank"
          rel="noopener noreferrer"
        >
          Quinn Leary
        </a>
      </footer>
    </div>
  );
}
