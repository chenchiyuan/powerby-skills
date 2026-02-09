```mermaid
flowchart LR
    subgraph TODO[ToDo]
        T1[Task-001]\n优先级: P0\n状态: ToDo
        T2[Task-002]\n优先级: P1\n状态: ToDo
    end

    subgraph DOING[Doing]
        T3[Task-003]\n优先级: P0\n状态: Doing
    end

    subgraph DONE[Done]
        T4[Task-004]\n优先级: P2\n状态: Done
    end

    T1 --> T3
    T2 --> T3
    T3 --> T4
```
