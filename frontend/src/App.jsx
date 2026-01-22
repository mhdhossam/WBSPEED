import { sendConvex } from "./wasmApi";

export default function App() {
  return (
    <div>
      <button onClick={async () => {
        console.log(
          await sendConvex("/api/messages/add/", { content: "Hello" })
        );
      }}>
        Add
      </button>

      <button onClick={async () => {
        console.log(
          await sendConvex("/api/messages/list/", { limit: 5 })
        );
      }}>
        List
      </button>
    </div>
  );
}
