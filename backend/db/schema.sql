create table if not exists books (
  id text primary key,
  title text not null,
  genre text not null,
  series text,
  status text not null,
  created_at timestamptz not null default now()
);

create table if not exists pipeline_stages (
  id text primary key,
  book_id text not null references books(id),
  stage text not null,
  status text not null,
  progress integer not null default 0,
  updated_at timestamptz not null default now()
);

create table if not exists documents (
  id text primary key,
  book_id text not null references books(id),
  name text not null,
  status text not null,
  content text,
  created_at timestamptz not null default now()
);

create table if not exists agent_activities (
  id text primary key,
  book_id text not null references books(id),
  message text not null,
  created_at timestamptz not null default now()
);

create table if not exists chat_messages (
  id text primary key,
  book_id text not null references books(id),
  role text not null,
  content text not null,
  created_at timestamptz not null default now()
);

create table if not exists chapters (
  id text primary key,
  book_id text not null references books(id),
  number integer not null,
  title text not null,
  status text not null,
  content text not null,
  created_at timestamptz not null default now()
);
