"""
This demo shows how to set the limits of movement on a servo and then move between those positions
"""

try:
    from MicroServo import Servo
except ImportError:
    print("Failed to import MicroServo from python system path")
    print("Importing from parent folder instead")
    try:
        import sys
        sys.path.append("..")
        from MicroServo import Servo
    except ImportError:
        raise ImportError(
            "Failed to import library from parent folder")


def main():
  s = Servo(100);
  while 1==1 :
    for i in range(0,180) :
      s._set_angle(i)
      s.turn()

if __name__ == "__main__":
    main()
