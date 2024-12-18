class ᱹᱹᱹᱹᱹᱹᱹᱹᱹ(Exception):
  pass

class ᱹᱹᱹ:
  def __init__(ᱹᱹᱹᱹ, ᱹ: "ᱹᱹ", ᱹᱹ: int, ᱹᱹᱹ: int):
    ᱹᱹᱹᱹ.__ᱹ__ = ᱹ
    ᱹᱹᱹᱹ.__ᱹᱹ__ = ᱹᱹ
    ᱹᱹᱹᱹ.__ᱹᱹᱹ__ = ᱹᱹᱹ
    ᱹᱹᱹᱹ.__ᱹᱹᱹᱹᱹ__ = {}

  def __getattr__(ᱹᱹᱹᱹ, ᱹᱹ: str):
    if ᱹᱹ in ᱹᱹᱹᱹ.__ᱹᱹᱹᱹᱹ__:
      ᱹ.ᱹ = ᱹᱹᱹᱹ.__ᱹᱹᱹᱹᱹ__[ᱹᱹ]
      return ᱹ
    ᱹᱹᱹ = list(ᱹᱹ)
    if not all(ᱹ == "ᱹ" for ᱹ in ᱹᱹᱹ):
      raise ᱹᱹᱹᱹᱹᱹᱹᱹᱹ(f"I mean, this is dot script, right? So, why are you using this {ᱹ} instead of ᱹ? This is very confusing.")
    ᱹᱹᱹ = ᱹᱹᱹᱹ.__ᱹᱹ__ + len(ᱹᱹᱹ) - 1
    if ᱹᱹᱹ > ᱹᱹᱹᱹ.__ᱹᱹᱹ__:
      raise ᱹᱹᱹᱹᱹᱹᱹᱹᱹ("You tried to access a value that is beyond your control. You might miscounted the number of ᱹ in your code.")
    ᱹᱹᱹᱹ.__ᱹᱹᱹᱹᱹ__[ᱹᱹ] = chr(ᱹᱹᱹ)
    ᱹ.ᱹ = chr(ᱹᱹᱹ)
    return ᱹ



ᱹᱹᱹᱹᱹ = ""

class ᱹᱹ:
  def __init__(ᱹᱹᱹᱹ):
    global ᱹᱹᱹᱹᱹ
    ᱹᱹᱹᱹᱹ = ""
    ᱹᱹᱹᱹ.ᱹᱹ = ᱹᱹᱹ(ᱹᱹᱹᱹ, 97, 122); # a-z
    ᱹᱹᱹᱹ.ᱹᱹᱹ = ᱹᱹᱹ(ᱹᱹᱹᱹ, 65, 90); # A-Z
    ᱹᱹᱹᱹ.ᱹᱹᱹᱹ = ᱹᱹᱹ(ᱹᱹᱹᱹ, 48, 57); # 0-9
    ᱹᱹᱹᱹ.ᱹᱹᱹᱹᱹ = ᱹᱹᱹ(ᱹᱹᱹᱹ, 42, 47); # *+,-./
    ᱹᱹᱹᱹ.ᱹᱹᱹᱹᱹᱹ = ᱹᱹᱹ(ᱹᱹᱹᱹ, 32, 41); #  !"#$%&'()
    ᱹᱹᱹᱹ.ᱹᱹᱹᱹᱹᱹᱹ = ᱹᱹᱹ(ᱹᱹᱹᱹ, 91, 96); # []^_`
    ᱹᱹᱹᱹ.ᱹᱹᱹᱹᱹᱹᱹᱹ = ᱹᱹᱹ(ᱹᱹᱹᱹ, 58, 64); # :;<=>?@
    ᱹᱹᱹᱹ.ᱹᱹᱹᱹᱹᱹᱹᱹᱹ = ᱹᱹᱹ(ᱹᱹᱹᱹ, 123, 126); # {|}~

  @property
  def ᱹ(ᱹᱹᱹᱹ):
    return ᱹᱹᱹᱹ.ᱹ
  
  @ᱹ.setter
  def ᱹ(ᱹᱹᱹᱹ, ᱹ):
    global ᱹᱹᱹᱹᱹ
    ᱹᱹᱹᱹᱹ += ᱹ

  @ᱹ.getter
  def ᱹ(ᱹᱹᱹᱹ):
    eval(ᱹᱹᱹᱹᱹ)
  
  @ᱹ.deleter
  def ᱹ(ᱹᱹᱹᱹ):
    raise AttributeError("ᱹᱹ.ᱹ is not deletable")


ᱹ = ᱹᱹ()
