create table if not exists public.word_planet_app_state (
  id text primary key,
  state_json jsonb not null default '{}'::jsonb,
  updated_at timestamptz not null default timezone('utc', now())
);

alter table public.word_planet_app_state enable row level security;

drop policy if exists "public read word planet state" on public.word_planet_app_state;
create policy "public read word planet state"
on public.word_planet_app_state
for select
to anon
using (true);

drop policy if exists "public insert word planet state" on public.word_planet_app_state;
create policy "public insert word planet state"
on public.word_planet_app_state
for insert
to anon
with check (true);

drop policy if exists "public update word planet state" on public.word_planet_app_state;
create policy "public update word planet state"
on public.word_planet_app_state
for update
to anon
using (true)
with check (true);

insert into storage.buckets (id, name, public)
values ('word-planet-audio', 'word-planet-audio', true)
on conflict (id) do nothing;

drop policy if exists "public read word planet audio" on storage.objects;
create policy "public read word planet audio"
on storage.objects
for select
to anon
using (bucket_id = 'word-planet-audio');

drop policy if exists "public upload word planet audio" on storage.objects;
create policy "public upload word planet audio"
on storage.objects
for insert
to anon
with check (bucket_id = 'word-planet-audio');

drop policy if exists "public delete word planet audio" on storage.objects;
create policy "public delete word planet audio"
on storage.objects
for delete
to anon
using (bucket_id = 'word-planet-audio');
