const anim = new Manim("#animation");

anim.scene(() => {
  const caption = document.getElementById("caption");
  caption.textContent = "Perfect Competition – all three points coincide";

  const axes = anim.axes({ x: { min:0, max:200 }, y: { min:0, max:200 }, color: "#666" });
  const ATC = anim.curve(q => 50 + 1000/q + 0.01*q*q, { stroke: "#1f77b4", strokeWidth: 5 });
  const MC  = anim.curve(q => 50 + 0.02*q, { stroke: "#ff7f0e", strokeWidth: 5 });
  const Pcomp = anim.line([[0,90],[200,90]], { stroke: "#2ca02c", strokeWidth: 5 });
  const singleDot = anim.circle([100,90], 0.18, { fill: "#9467bd" });

  anim.play([ATC.fadeIn(), MC.fadeIn(), Pcomp.fadeIn(), singleDot.fadeIn()], 2);
  anim.wait(2);
  anim.text("All three coincide here", [100,60], { fill: "#9467bd", fontSize: 28 }).fadeIn(1);
  anim.wait(3);

  caption.textContent = "Now the same industry becomes a monopoly…";
  anim.play(Pcomp.fadeOut(), 1.5);

  const demand = anim.line([[0,200],[200,0]], { stroke: "#d62728", strokeWidth: 5 });
  const MR = anim.line([[0,200],[100,0]], { stroke: "#d62728", strokeWidth: 5, strokeDasharray: "10 8" });
  anim.play([demand.fadeIn(), MR.fadeIn()], 2);

  caption.textContent = "Watch the three points tear apart!";
  const profitDot = anim.circle([75,125], 0.18, { fill: "#e377c2" });
  const minATCDot = anim.circle([100,90], 0.18, { fill: "#1f77b4" });
  const socialDot = anim.circle([150,90], 0.18, { fill: "#2ca02c" });

  anim.play(singleDot.moveTo([75,125]), singleDot.change({fill: "#e377c2"}), minATCDot.fadeIn(), socialDot.fadeIn(), 3);

  const dwl = anim.polygon([[75,125],[150,90],[150,125]], { fill: "#ff9999", opacity: 0.7 });
  anim.play(dwl.fadeIn(), 1.5);

  caption.textContent = "Monopoly: three separate points = inefficiency + rents";
  anim.text("Profit-max Q", [75,140], { fill: "#e377c2", fontSize: 26 }).fadeIn();
  anim.text("Min efficient scale", [100,70], { fill: "#1f77b4", fontSize: 26 }).fadeIn();
  anim.text("Social optimum", [150,70], { fill: "#2ca02c", fontSize: 26 }).fadeIn();
  anim.wait(6);
});
