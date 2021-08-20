// define the time limit
let TIME_LIMIT = 60;

// define arrays to be used
let js_array = [
  'let x = 2;',
  'let y = 2;',
  'let xy = x * y;',
  'console.log(xy);',
  'const [username, setUsername] = useState("");',
  'const [email, setEmail] = useState("");',
  'const [password, setPassword] = useState("");',
  'const [confirmpassword, setConfirmPassword] = useState("");',
  'const [error, setError] = useState("");',
  'let cpm_text = document.querySelector(".curr_cpm");',
  'let restart_btn = document.querySelector(".restart_btn");',
  'return next(new ErrorResponse("Not authorized to access this router", 401));',
  'token = req.headers.authorization.split(" ")[1];',
  'error = new ErrorResponse(message, 400);',
  'const message = Object.values(err.errors).map((val) => val.message);',
  'error.message = err.message;'
];

let py_array = [
  'nameInput = input("enter your name")',
  'print("Hello + nameInput")',
  'def iscoroutinefunction(func: t.Any) -> bool:',
  'while inspect.ismethod(func):',
  'static_url_path: t.Optional[str] = None,',
  'static_folder: t.Optional[t.Union[str, os.PathLike]] = "static",',
  'static_host: t.Optional[str] = None,',
  'host_matching: bool = False,',
  'subdomain_matching: bool = False,',
  'template_folder: t.Optional[str] = "templates",',
  'instance_path: t.Optional[str] = None,',
  'instance_relative_config: bool = False,',
  'import_name=import_name,',
  'if instance_path is None:',
  'instance_path = self.auto_find_instance_path()',
  'template_rendered = _signals.signal("template-rendered")',
  'before_render_template = _signals.signal("before-render-template")'

];

let java_array = [
  'System.out.println("Hello world");',
  'Integer.parseInt("400");',
  'import java.util.*;',
  'public static void main(String[] args)',
  'Math.pow(4,8);',
  'String num = String.valueOf(5);',
  'java.util.Date = java.text.DateFormat.getDateInstance().parse(date String)',
  'public class HelloWorld',
  'public void fetch() throws IOException',
  'Scanner sc = new Scanner(System.in);',
  'System.out.print("Hi no space.");',
  'for (int i = 0; i < 100; i++)',
  'int i = sc.nextInt();',
  'while(int i < 0)',
  'String text = "Hello!";',
  'if (text != null)',
  'private static Integer returnInt()',
  'return num;',
  'int x = 6008;',
  'Double result = x/num;'
];

// selecting required elements
let timer_text = document.querySelector(".curr_time");
let accuracy_text = document.querySelector(".curr_accuracy");
let error_text = document.querySelector(".curr_errors");
let cpm_text = document.querySelector(".curr_cpm");
let wpm_text = document.querySelector(".curr_wpm");
let quote_text = document.querySelector(".quote");
let input_area = document.querySelector(".input_area");
let restart_btn = document.querySelector(".restart_btn");
let cpm_group = document.querySelector(".cpm");
let wpm_group = document.querySelector(".wpm");
let error_group = document.querySelector(".errors");
let accuracy_group = document.querySelector(".accuracy");

let timeLeft = TIME_LIMIT;
let timeElapsed = 0;
let total_errors = 0;
let errors = 0;
let accuracy = 0;
let characterTyped = 0;
let current_quote = "";
let quoteNo = 0;
let timer = null;

const select = document.querySelector("#language-select");

function updateQuote() {

  if (select.value === "Python") {
    quote_text.textContent = null;
    current_quote = py_array[quoteNo];

    // separate each character and make an element
    // out of each of them to individually style them
    current_quote.split("").forEach((char) => {
      const charSpan = document.createElement("span");
      charSpan.innerText = char;
      quote_text.appendChild(charSpan);
    });

    // roll over to the first quote
    if (quoteNo < py_array.length - 1) quoteNo++;
    else quoteNo = 0;
  } else if (select.value == "Javascript") {
    quote_text.textContent = null;
    current_quote = js_array[quoteNo];

    // separate each character and make an element
    // out of each of them to individually style them
    current_quote.split("").forEach((char) => {
      const charSpan = document.createElement("span");
      charSpan.innerText = char;
      quote_text.appendChild(charSpan);
    });

    // roll over to the first quote
    if (quoteNo < js_array.length - 1) quoteNo++;
    else quoteNo = 0;
  } else {
    quote_text.textContent = null;
    current_quote = java_array[quoteNo];

    // separate each character and make an element
    // out of each of them to individually style them
    current_quote.split("").forEach((char) => {
      const charSpan = document.createElement("span");
      charSpan.innerText = char;
      quote_text.appendChild(charSpan);
    });

    // roll over to the first quote
    if (quoteNo < java_array.length - 1) quoteNo++;
    else quoteNo = 0;
  }
}

function processCurrentText() {
  // get current input text and split it
  curr_input = input_area.value;
  curr_input_array = curr_input.split("");

  // increment total characters typed
  characterTyped++;

  errors = 0;

  quoteSpanArray = quote_text.querySelectorAll("span");
  quoteSpanArray.forEach((char, index) => {
    let typedChar = curr_input_array[index];

    // characters not currently typed
    if (typedChar == null) {
      char.classList.remove("correct_char");
      char.classList.remove("incorrect_char");

      // correct characters
    } else if (typedChar === char.innerText) {
      char.classList.add("correct_char");
      char.classList.remove("incorrect_char");

      // incorrect characters
    } else {
      char.classList.add("incorrect_char");
      char.classList.remove("correct_char");

      // increment number of errors
      errors++;
    }
  });

  // display the number of errors
  error_text.textContent = total_errors + errors;

  // update accuracy text
  let correctCharacters = characterTyped - (total_errors + errors);
  let accuracyVal = (correctCharacters / characterTyped) * 100;
  accuracy_text.textContent = Math.round(accuracyVal);

  // if current text is completely typed
  // irrespective of errors
  if (curr_input.length == current_quote.length) {
    updateQuote();

    // update total errors
    total_errors += errors;

    // clear the input area
    input_area.value = "";
  }
}

function updateTimer() {
  if (timeLeft > 0) {
    // decrease the current time left
    timeLeft--;

    // increase the time elapsed
    timeElapsed++;

    // update the timer text
    timer_text.textContent = timeLeft + "s";
  } else {
    // finish the game
    finishGame();
  }
}

function finishGame() {
  // stop the timer
  clearInterval(timer);

  // disable the input area
  input_area.disabled = true;

  // show finishing text
  quote_text.textContent = "Click on restart to start a new game.";

  // display restart button
  restart_btn.style.display = "block";

  // calculate cpm and wpm
  cpm = Math.round((characterTyped / timeElapsed) * 60);
  wpm = Math.round((characterTyped / 5 / timeElapsed) * 60);

  // update cpm and wpm text
  cpm_text.textContent = cpm;
  wpm_text.textContent = wpm;

  // display the cpm and wpm
  cpm_group.style.display = "block";
  wpm_group.style.display = "block";
}

function startGame() {

  timeleft = TIME_LIMIT;
  input_area.placeholder = " ";
  updateQuote();

  // clear old and start a new timer
  clearInterval(timer);
  timer = setInterval(updateTimer, 1000);
}

function resetValues() {
  timeLeft = TIME_LIMIT;
  clearInterval(timer);
  timeElapsed = 0;
  errors = 0;
  total_errors = 0;
  accuracy = 0;
  characterTyped = 0;
  quoteNo = 0;
  input_area.disabled = false;

  input_area.value = "";
  input_area.placeholder = "Click here to start...";
  quote_text.textContent = "Click on the area below to start a new session";
  accuracy_text.textContent = "--";
  timer_text.textContent = timeLeft + "s";
  error_text.textContent = 0;
  cpm_text.textContent = "--";
  wpm_text.textContent = "--";
  cpm_group.style.display = "none";
  wpm_group.style.display = "none";
}

/* When the user clicks on the button,
toggle between hiding and showing the dropdown content */
function myFunction() {
  document.getElementById("myDropdown").classList.toggle("show");
}

// Close the dropdown menu if the user clicks outside of it
window.onclick = function (event) {
  if (!event.target.matches(".dropbtn")) {
    var dropdowns = document.getElementsByClassName("dropdown-content");
    var i;
    for (i = 0; i < dropdowns.length; i++) {
      var openDropdown = dropdowns[i];
      if (openDropdown.classList.contains("show")) {
        openDropdown.classList.remove("show");
      }
    }
  }
};
