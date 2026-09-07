import React, { useEffect, useState } from "react";
import axios from "axios";

const API_URL = "http://127.0.0.1:8000";

function App() {
  const [task, setTask] = useState("");
  const [tasks, setTasks] = useState([]);
  const [plan, setPlan] = useState([]);
  const [memory, setMemory] = useState([]);

  const [changedTask, setChangedTask] = useState("");
  const [changeReason, setChangeReason] = useState("");

  const [loading, setLoading] = useState(false);
  const [planning, setPlanning] = useState(false);
  const [monitoring, setMonitoring] = useState(false);

  const [message, setMessage] = useState("");

  useEffect(() => {
    loadTasks();
    loadMemory();
  }, []);

  const loadTasks = async () => {
    try {
      const response = await axios.get(`${API_URL}/tasks`);
      setTasks(response.data);
    } catch (error) {
      console.error(error);
      setMessage("Could not load tasks.");
    }
  };

  const loadMemory = async () => {
    try {
      const response = await axios.get(`${API_URL}/memory`);
      setMemory(response.data);
    } catch (error) {
      console.error(error);
    }
  };

  const addTask = async () => {
    if (!task.trim()) {
      setMessage("Please enter a task.");
      return;
    }

    setLoading(true);
    setMessage("");

    try {
      const response = await axios.post(`${API_URL}/tasks`, {
        text: task
      });

      if (response.data.error) {
        setMessage(response.data.error);
      } else {
        setMessage("Task added successfully.");
        setTask("");
        await loadTasks();
      }
    } catch (error) {
      console.error(error);
      setMessage("Could not add task.");
    }

    setLoading(false);
  };

 const clearTasks = async () => {
  try {
    await axios.delete(`${API_URL}/tasks`);

    setTasks([]);
    setPlan([]);
    setMemory([]);
    setChangedTask("");
    setChangeReason("");

    setMessage(
      "Tasks, agent memory and schedule cleared."
    );

  } catch (error) {
    console.error(error);
    setMessage("Could not clear tasks.");
  }
};

  const createPlan = async () => {
    setPlanning(true);
    setMessage("");

    try {
      const response = await axios.post(`${API_URL}/analyze`);

      setPlan(response.data.plan || []);
      await loadMemory();

      setMessage("AI plan created successfully.");
    } catch (error) {
      console.error(error);
      setMessage("Could not create AI plan.");
    }

    setPlanning(false);
  };

  const monitorSchedule = async () => {
    setMonitoring(true);
    setMessage("");

    try {
      const response = await axios.post(`${API_URL}/monitor`);

      setPlan(response.data.plan || []);
      await loadTasks();
      await loadMemory();

      if (response.data.replanned) {
        setMessage("Problem detected. Agent automatically replanned.");
      } else {
        setMessage("Schedule is safe.");
      }
    } catch (error) {
      console.error(error);
      setMessage("Could not monitor schedule.");
    }

    setMonitoring(false);
  };

  const replanSchedule = async () => {
    if (!changedTask || !changeReason.trim()) {
      setMessage("Select a task and describe the change.");
      return;
    }

    setMessage("Replanning schedule...");

    try {
      const response = await axios.post(`${API_URL}/replan`, {
        reason: changeReason,
        changed_task: changedTask
      });

      setPlan(response.data.plan || []);

      await loadTasks();
      await loadMemory();

      setChangeReason("");

      setMessage("Schedule replanned successfully.");
    } catch (error) {
      console.error(error);
      setMessage("Could not replan schedule.");
    }
  };

  const completeTask = async (taskName) => {
    try {
      await axios.post(`${API_URL}/tasks/complete`, {
        name: taskName
      });

      await loadTasks();

      setMessage("Task completed successfully.");
    } catch (error) {
      console.error(error);
      setMessage("Could not complete task.");
    }
  };

  return (
    <div className="app">

      <header className="header">
        <div>
          <h1>Deadline Rescue Agent</h1>
          <p>AI-powered deadline management and adaptive planning</p>
        </div>

        <div className="status">
          Agent Status: Ready
        </div>
      </header>

      <main className="container">

        {/* ADD TASK */}

        <section className="card">
          <h2>Add Task</h2>

          <p className="description">
            Describe your task naturally. The AI extracts the deadline,
            duration and importance.
          </p>

          <div className="input-area">
            <input
              type="text"
              placeholder="Example: Complete project by tomorrow 5 PM, takes 3 hours, very important"
              value={task}
              onChange={(e) => setTask(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === "Enter") {
                  addTask();
                }
              }}
            />

            <button
              onClick={addTask}
              disabled={loading}
            >
              {loading ? "Adding..." : "Add Task"}
            </button>
          </div>

          {message && (
            <p className="message">
              {message}
            </p>
          )}
        </section>


        {/* TASKS */}

        <section className="card">

          <div className="section-header">
            <div>
              <h2>Your Tasks</h2>
              <p className="description">
                Tasks currently managed by the agent.
              </p>
            </div>

            <div>
              <button
                className="secondary-button"
                onClick={loadTasks}
              >
                Refresh
              </button>

              <button
                className="secondary-button"
                onClick={clearTasks}
              >
                Clear Tasks
              </button>
            </div>
          </div>

          {tasks.length === 0 ? (

            <div className="empty">
              No tasks available.
            </div>

          ) : (

            <div className="task-list">

              {tasks.map((item, index) => (

                <div className="task" key={index}>

                  <div>
                    <h3>{item.name}</h3>

                    <p>
                      Deadline: {item.deadline}
                    </p>

                    <p>
                      Duration: {item.duration} hours
                    </p>
                  </div>

                  <div className="task-details">

                    <span>
                      Importance: {item.importance}/5
                    </span>

                    {item.priority !== undefined && (
                      <span>
                        Priority: {item.priority}
                      </span>
                    )}

                    {!item.completed && (
                      <button
                        className="secondary-button"
                        onClick={() =>
                          completeTask(item.name)
                        }
                      >
                        Complete
                      </button>
                    )}

                    {item.completed && (
                      <span>
                        Completed
                      </span>
                    )}

                  </div>

                </div>

              ))}

            </div>

          )}

        </section>


        {/* AI PLANNING */}

        <section className="card">

          <div className="section-header">

            <div>
              <h2>AI Schedule</h2>

              <p className="description">
                The agent reasons about task urgency, importance,
                duration and deadlines.
              </p>
            </div>

            <div>
              <button
                onClick={createPlan}
                disabled={planning}
              >
                {planning ? "Planning..." : "Create AI Plan"}
              </button>

              <button
                className="secondary-button"
                onClick={monitorSchedule}
                disabled={monitoring}
              >
                {monitoring
                  ? "Monitoring..."
                  : "Monitor Schedule"}
              </button>
            </div>

          </div>


          {plan.length === 0 ? (

            <div className="empty">
              No schedule created yet.
            </div>

          ) : (

            <div className="plan-list">

              {plan.map((item, index) => (

                <div className="plan-item" key={index}>

                  <div className="plan-number">
                    {index + 1}
                  </div>

                  <div className="plan-content">

                    <h3>
                      {item.task}
                    </h3>

                    <p>
                      Start: {item.start}
                    </p>

                    <p>
                      End: {item.end}
                    </p>

                    <p>
                      Deadline: {item.deadline}
                    </p>

                    <p>
                      Priority: {item.priority}
                    </p>

                  </div>

                  <span
                    className={
                      item.status === "At Risk"
                        ? "risk"
                        : "safe"
                    }
                  >
                    {item.status}
                  </span>

                </div>

              ))}

            </div>

          )}

        </section>


        {/* MANUAL REPLAN */}

        <section className="card">

          <h2>Schedule Change</h2>

          <p className="description">
            Tell the agent about a change. It will reconsider
            the schedule and create a new plan.
          </p>

          <div className="replan-area">

            <select
              value={changedTask}
              onChange={(e) =>
                setChangedTask(e.target.value)
              }
            >
              <option value="">
                Select task
              </option>

              {tasks.map((item, index) => (
                <option
                  key={index}
                  value={item.name}
                >
                  {item.name}
                </option>
              ))}

            </select>

            <input
              type="text"
              placeholder="Example: This task will take 2 hours longer"
              value={changeReason}
              onChange={(e) =>
                setChangeReason(e.target.value)
              }
            />

            <button onClick={replanSchedule}>
              Replan
            </button>

          </div>

        </section>


        {/* AGENT FLOW */}

        <section className="card">

          <h2>Agent Decision Flow</h2>

          <p className="description">
            How the Deadline Rescue Agent operates.
          </p>

          <div className="agent-flow">

            <div>Observe</div>
            <span>→</span>

            <div>Reason</div>
            <span>→</span>

            <div>Decide</div>
            <span>→</span>

            <div>Act</div>
            <span>→</span>

            <div>Monitor</div>
            <span>→</span>

            <div>Replan</div>
            <span>→</span>

            <div>Remember</div>

          </div>

        </section>


        {/* MEMORY */}

        <section className="card">

          <h2>Agent Memory</h2>

          <p className="description">
            Previous decisions and schedule changes recorded
            by the agent.
          </p>

          {memory.length === 0 ? (

            <div className="empty">
              No agent activity recorded yet.
            </div>

          ) : (

            <div className="plan-list">

              {memory.map((event, index) => (

                <div className="plan-item" key={index}>

                  <div className="plan-number">
                    {index + 1}
                  </div>

                  <div className="plan-content">

                    <h3>
                      {event.event}
                    </h3>

                    {event.reason && (
                      <p>
                        Reason: {event.reason}
                      </p>
                    )}

                    {event.changed_task && (
                      <p>
                        Changed Task: {event.changed_task}
                      </p>
                    )}

                    {event.decision && (
                      <p>
                        AI Action: {event.decision.action}
                      </p>
                    )}

                  </div>

                </div>

              ))}

            </div>

          )}

        </section>

      </main>

    </div>
  );
}

export default App;