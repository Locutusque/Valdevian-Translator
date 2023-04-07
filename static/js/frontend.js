var timer;
    
        $(document).ready(function() {
            $("#input_text").on("input", function() {
                clearTimeout(timer);
                timer = setTimeout(sendRequest, 500);
            });
        });
    
        function sendRequest() {
          $("#output_text").empty();
          var input_text = $("#input_text").val().trim();
          var model_input = $("#model-select").val()
          if (input_text.length > 0) {
              $(".loader").show();
              $.post("/translate", {"input_text": input_text, "model": model_input}, function(data) {
                  console.log(data)
                  $(".loader").hide();
                  startTypingAnimation(data);
              });
          }
      }
      
    
        var typing = null;
var cursorVisible = false;

function startTypingAnimation(text) {
  var chars = text.split("");
  var i = 0;
  typing = setInterval(function() {
    if (i == chars.length) {
      stopTypingAnimation();
      return;
    }
    var char = chars[i];
    $("#output_text").text($("#output_text").text() + char);
    i++;
  }, 50);
}

function stopTypingAnimation() {
  clearInterval(typing);
  typing = null;
}
const t5SmallReq = "CPU: Quad-core 2.5 GHz or better<br>RAM: 16 GB or higher<br>Storage: 40 GB or more available space on a solid-state drive (SSD)<br>GPU: NVIDIA GeForce GTX 1080 or better<br>Operating System: 64-bit Windows 10 or Linux";
const t5BaseReq = "CPU: Octa-core 2.5 GHz or better<br>RAM: 32 GB or higher<br>Storage: 80 GB or more available space on a solid-state drive (SSD)<br>GPU: NVIDIA GeForce GTX 1080 or better<br>Operating System: 64-bit Windows 10 or Linux";
const t5LargeReq = "CPU: Octa-core 2.5 GHz or better<br>RAM: 32 GB or higher<br>Storage: 80 GB or more available space on a solid-state drive (SSD)<br>GPU: NVIDIA A100 or better<br>Operating System: 64-bit Linux";
const t53bReq = "CPU: 64-core 2.5 GHz or better<br>RAM: 256 GB or higher<br>Storage: 2 TB or more available space on a solid-state drive (SSD)<br>GPU: NVIDIA A100 or better<br>Operating System: 64-bit Linux";
const t511bReq = "CPU: 128-core 2.5 GHz or better<br>RAM: 1024 GB or higher<br>Storage: 10 TB or more available space on a solid-state drive (SSD)<br>GPU: NVIDIA A100 or better<br>Operating System: 64-bit Linux";

const dropdown = document.getElementById("model-select");
const sysReqs = document.getElementById("sys_reqs");

dropdown.addEventListener("change", (event) => {
  const selectedModel = event.target.value;
  let requirements;

  if (selectedModel === "t5-small") {
    requirements = t5SmallReq;
  } else if (selectedModel === "t5-base") {
    requirements = t5BaseReq;
  } else if (selectedModel === "t5-large") {
    requirements = t5LargeReq;
  } else if (selectedModel === "t5-3b") {
    requirements = t53bReq;
  } else if (selectedModel === "t5-11b") {
    requirements = t511bReq;
  }

  sysReqs.innerHTML = requirements;
});
function trainModel() {
  var model = $("#model-select").val().trim();
  console.log("Model selected:", model);
  $.post("/train", {"model": model})
      .done(function(response) {
          console.log("Training complete:", response);
      })
      .fail(function(error) {
          console.log("Training failed:", error);
      });
}

