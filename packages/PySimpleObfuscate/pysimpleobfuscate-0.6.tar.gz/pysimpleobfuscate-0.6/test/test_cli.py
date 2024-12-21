import unittest
import subprocess
import io

class TestCLI(unittest.TestCase):

    def tearDown(self):
        subprocess.run(["rm", "-rf", "src/test/dist"]) 

    def test_obfuscate_file(self):

        subprocess.run(["python3", "src/lib/cli.py", "--msg", "encrypted files test", "--dest", "src/test/dist/hello.py", "src/test/fixtures/hello.py"]) 
        
        proc = subprocess.Popen(["python3", "src/test/dist/hello.py"], stdout=subprocess.PIPE)

        with io.TextIOWrapper(proc.stdout, encoding="utf-8") as out:
            for line in out:
                self.assertEqual(line.strip(), "hello")

        proc.kill()

    def test_obfuscate_folder(self):
        
        subprocess.run(["python3", "src/lib/cli.py", "--msg", "encrypted files test", "--dest", "src/test/dist", "src/test/fixtures"]) 
        
        proc = subprocess.Popen(["python3", "src/test/dist/world.py"], stdout=subprocess.PIPE)

        with io.TextIOWrapper(proc.stdout, encoding="utf-8") as out:
            for line in out:
                self.assertEqual(line.strip(), "hello")

        proc.kill()


if __name__ == "__main__":
    unittest.main()