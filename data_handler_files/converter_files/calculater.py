

def calculate(info,start):
  fix_numbers=0.5,0.25
  h_gol=info[0]
  a_gol=info[1]
  h_xg=start
  a_xg=start
  h_pr=start
  a_pr=start
  pr_chaging=((h_gol-a_gol)-(h_pr-a_pr)-fix_numbers[0])*fix_numbers[1]
  xg_changing=((h_xg-a_xg)-(h_pr-a_pr)-fix_numbers[0])*fix_numbers[1]
  prxg_changing=((h_gol-a_gol)-(h_xg-a_xg)-(h_pr-a_pr)-fix_numbers[0])*fix_numbers[1]
  xg_changing=("%.4f" % xg_changing)
  prxg_changing=("%.4f" % prxg_changing)