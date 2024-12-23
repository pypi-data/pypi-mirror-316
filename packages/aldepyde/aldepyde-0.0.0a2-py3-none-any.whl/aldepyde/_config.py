import sys

class _config():
    def __init__(self):
        self.settings = {
            "verbose": False,
            "angle_mode": "degrees"
        }
        self._setters = {
            "verbose" : (self.SetVerbose, [True, False]),
            "angle_mode": (self.SetAngleMode, ["degrees", "radians"])
        }

    def _Verify(self, key, value) -> None:
        if value not in self._setters[key][1]:
            print(f"Incorrect value for ({key} <-- {value})\n\tAllowed values: {self._setters[key][1]}", file=sys.stderr)
            raise ValueError("See above")

    def __getitem__(self, item):
        return self.settings[item]
    def GetVerbose(self) -> bool:
        return self.settings['verbose']

    def SetVerbose(self, v: bool) -> None:
        self._Verify('verbose', v)
        self.settings['verbose'] = v


    def GetAngleMode(self) -> str:
        return self.settings['angle_mode']

    def SetAngleMode(self, a_type: str) -> None:
        self._Verify('angle_mode', a_type)
        self.settings['angle_mode'] = a_type

    def Load(self, s: dict) -> None:
        if set(s.keys()) != set(self._setters.keys()): # Mismatch in settings
            missing_settings = "".join([f"\t-{k} : {v[1]}\n" for k, v in self._setters.items() if k not in s.keys()])
            extra_settings = "".join([f"\t-{k}\n" for k in s.keys() if k not in self._setters.keys()])
            print(f"Input config does not match expectations.", file=sys.stderr)
            if len(missing_settings) != 0:
                print(f"Please include the following:\n{missing_settings}", end="", file=sys.stderr)
            if len(extra_settings) != 0:
                print(f"Please remove the following:\n{extra_settings}", file=sys.stderr)
            raise KeyError("See above")
        for key in self._setters.keys():
            self._setters[key][0](s[key])

    def GetConfig(self) -> dict:
        return self.settings

