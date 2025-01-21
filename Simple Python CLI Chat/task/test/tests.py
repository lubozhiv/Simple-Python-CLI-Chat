from hstest import dynamic_test, StageTest, CheckResult, TestedProgram
import re


class Test(StageTest):

    responses = []
    prompts = [
        {"prompt": "What is 5 + 10?", "answer": "15"},
        {"prompt": "What is the largest ocean?", "answer": "Pacific Ocean"},
        {"prompt": "What is 15 + 25?", "answer": "40"},
        {"prompt": "What is the capital of France?", "answer": "Paris"},
        {"prompt": "What is the capital of Germany?", "answer": "Berlin"},
        {"prompt": "How many days are in a week?", "answer": "7"},
        {"prompt": "What is the square root of 16?", "answer": "4"},
        {"prompt": "What is the square root of 9?", "answer": "3"},
        {"prompt": "Which color is this: #000?", "answer": "black"},
    ]

    @dynamic_test(time_limit=60000, data=prompts)
    def test1(self, run):
        prompt = run["prompt"]
        answer = run["answer"]

        program = TestedProgram()
        output = program.start().strip()

        # Check if output is "Enter a message: "
        if "Enter a message:" not in output:
            return CheckResult.wrong("The program should output 'Enter a message: ' after starting.")

        if not program.is_waiting_input():
            return CheckResult.wrong("The program should be waiting for input after starting.")

        output = program.execute(prompt).strip()

        # Check if output has the prompt with You:
        if 'You: ' + prompt not in output:
            return CheckResult.wrong("The prompt was not found in the output. You should output the prompt with 'You: ' before it.\nYour output:" + output )

        # Check if output has the assistant response with Assistant:
        if 'Assistant:' not in output:
            return CheckResult.wrong("The assistant response was not found in the output. You should output the assistant response with 'Assistant: ' before it.\nYour output:" + output)

        # Check if the response is correct
        if answer.lower() not in output.lower():
            return CheckResult.wrong("The assistant's response doesn't contain the expected answer for the prompt.\nYour output:" + output)

        # Check if output has the cost
        if not re.search(r'Cost: \$\d+\.\d+', output):
            return CheckResult.wrong("The cost was not found in the output. You should output the cost with 'Cost: $' before it.\nYour output:" + output)

        # Check if response is different from the previous one
        if output in self.responses:
            return CheckResult.wrong("The response is the same as the previous one. "
                                     "It should be different each time.")
        self.responses.append(output)

        return CheckResult.correct()


if __name__ == '__main__':
    Test('main').run_tests()