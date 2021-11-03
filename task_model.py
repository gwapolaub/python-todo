class Task:
  def __init__(self, name, category, reward_amt, expiration_sec, iteration, iteration_goal, iteration_expiration_sec,queued_dttm, start_dttm, completion_dttm):
    super().__init__()
    self.name = name
    self.category = category
    self.reward_amt = reward_amt
    self.expiration_sec = expiration_sec
    self.iteration = iteration
    self.iteration_goal = iteration_goal
    self.iteration_expiration_sec = iteration_expiration_sec
    self.queued_dttm = queued_dttm
    self.start_dttm = start_dttm
    self.completion_dttm = completion_dttm

