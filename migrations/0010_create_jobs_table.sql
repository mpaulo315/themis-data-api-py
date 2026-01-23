CREATE TABLE jobs (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    dataset_type VARCHAR(255) NOT NULL,
    resource_kind VARCHAR(255) NOT NULL,
    update_strategy VARCHAR(255) NOT NULL,
    cron_expression VARCHAR(255) NOT NULL,
    status INT DEFAULT 1, -- 1 = ativo, 0 = inativo
    runs INT,
    args JSONB,
    last_run_timestamp TIMESTAMP,
    execution_time_seconds BIGINT,
    last_success_timestamp TIMESTAMP,
    last_failure_timestamp TIMESTAMP,
    last_run_message TEXT,
    additional_info JSONB
);

DROP TABLE IF EXISTS jobs;
