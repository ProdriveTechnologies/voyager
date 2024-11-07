from click.testing import CliRunner
from voyager import voyager

def test_hello_world():
  runner = CliRunner()
  result = runner.invoke(voyager.search, ['InterfaceImplementations/PI.Swd'])
  print(result.output)

if __name__ == "__main__":
  test_hello_world()