class SMD3:
	def EmulatedValueDefault(self):
		"""Emulated value."""
		pass

	def Mode(self):
		"""Set or query the operating mode."""
		pass

	def JoystickMode(self):
		"""Set or query the joystick operation mode. Choose between single step or continuous rotation."""
		pass

	def UseExternalEnable(self):
		"""Set or query whether the external enable signal should be used."""
		pass

	def SensorSelect(self):
		"""Select termperature sensor. Choose between a K-Type thermocouple or a PT100 RTD."""
		pass

	def MotorTemperature(self):
		"""Query the motor temperature."""
		pass

	def RunCurrent(self):
		"""Set or query the motor run current, in Amps."""
		pass

	def HoldCurrent(self):
		"""Set or query the motor hold current, in Amps."""
		pass

	def PowerdownDelay(self):
		"""Set or query the delay time between standstill occurring and the motor current being reduced from the acceleration current to the hold current, in milliseconds."""
		pass

	def CurrentReductionDelay(self):
		"""Set or query the delay per current reduction step that occurs when run current is reduced to hold current, in milliseconds"""
		pass

	def Freewheel(self):
		"""Set or query the freewheel mode. Set the option to use passive braking or freewheeling when the motor is in standby."""
		pass

	def Resolution(self):
		"""Set or query the microstep resolution"""
		pass

	def BakeTemperature(self):
		"""Set or query the bake temperature setpoint."""
		pass

	def LimitsEnable(self):
		"""Set or query global enable of limits inputs."""
		pass

	def LimitPositiveEnable(self):
		"""Set or query enable of the positive limit."""
		pass

	def LimitNegativeEnable(self):
		"""Set or query enable of the negative limit."""
		pass

	def LimitPositivePolarity(self):
		"""Set or query polarity of the positive limit."""
		pass

	def LimitNegativePolarity(self):
		"""Set or query polarity of the negative limit."""
		pass

	def LimitsStopMode(self):
		"""Set or query the stop mode, determines behaviour when a limit is triggered."""
		pass

	def Acceleration(self):
		"""Set or query the motor acceleration, in Hz/s."""
		pass

	def Deceleration(self):
		"""Set or query the motor deceleration, in Hz/s."""
		pass

	def StartFrequency(self):
		"""Set or query the start frequency, in Hz."""
		pass

	def StopFrequency(self):
		"""Set or query the stop frequency, in Hz."""
		pass

	def StepFrequency(self):
		"""Set or query the target step frequency, in Hz."""
		pass

	def ActualStepFrequency(self):
		"""query the actual step frequency, in Hz."""
		pass

	def ActualPosition(self):
		"""Set or query the actual position, in steps. Argument range between [-8388608, +8388607] steps."""
		pass

	def StepEdge(self):
		"""Set or query a value indicating whether a step occurs on both the rising and falling edges of the step input, or just the rising edge."""
		pass

	def StepInterpolation(self):
		"""Set or query a value indicating whether the step input should be interpolated to 256 microsteps."""
		pass

	def Load(self):
		"""Load saved configuration."""
		pass

	def Store(self):
		"""Store configuration."""
		pass

	def Stop(self):
		"""Command motor to stop moving according to the current profile."""
		pass

	def MicrostepTransition(self):
		"""Set or query the full step / microstepping transition, in Hz."""
		pass

	def Clear(self):
		"""Clear faults."""
		pass

	def Serial(self):
		"""Query the serial number."""
		pass

	def ZerowaitTime(self):
		"""Set or query the waiting time after ramping down to a stop before the next movement can start, in milliseconds."""
		pass

	def JoystickAutoSelect(self):
		"""Set or query auto switching to joystick mode."""
		pass

	def Identify(self):
		"""Set or query enable blinking of that status indicator to aid in identifying the SMD3 among others."""
		pass

	def MoveAbsolute(self):
		"""Command to move the motor to an absolute position using the positioning mode.  Argument range between [-8388607, +8388607] steps."""
		pass

	def MoveRelative(self):
		"""Command to move the motor to a relative position using the positioning mode. Argument range between [-8388607, +8388607] steps."""
		pass

	def MoveVelocity(self):
		"""Command to move the motor using velocity mode.  Set "+" for positive direction or "-" for negative direction."""
		pass

	def EmergencyStop(self):
		"""Command stops immediately and disables the motor."""
		pass

	def AccelerationCurrent(self):
		"""Set or query the motor acceleration/deceleration current."""
		pass

	def RelativePosition(self):
		"""Set or query the relative position, in steps. Argument range between [-8388608, +8388607] steps."""
		pass

	def StartBake(self):
		"""Command to start the bake mode."""
		pass

	def StartHome(self):
		"""Command to start the home procedure. Set "+" for positive direction or "-" for negative direction."""
		pass

	def QuickStop(self):
		"""Command motor to stop the motion in 1 second."""
		pass

	def LimitsPolarity(self):
		"""Set the polarity for both positve and negative limits."""
		pass

	def FactoryReset(self):
		"""Load factory defaults."""
		pass

	def FirmwareVersion(self):
		"""Query the firmware version number."""
		pass

	def Flag(self):
		"""Get the error or status flags."""
		pass

	def TemperatureSensorShorted(self):
		"""Selected temperature sensor is short-circuited."""
		pass

	def TemperatureSensorOpen(self):
		"""Selected temperature sensor is open circuit."""
		pass

	def MotorOverTemperature(self):
		"""Selected temperature sensor is reporting temperature > 190 °C."""
		pass

	def MotorShort(self):
		"""Motor phase to phase or phase to ground short has been detected."""
		pass

	def ExternalInhibit(self):
		"""Motor disabled via external input."""
		pass

	def ConfigurationError(self):
		"""Motor configuration is corrupted."""
		pass

	def JoystickConnected(self):
		"""Joystick is connected."""
		pass

	def LimitNegative(self):
		"""Limit negative input is active."""
		pass

	def LimitPositive(self):
		"""Limit positive input is active"""
		pass

	def ExternalEnable(self):
		"""External enable input state."""
		pass

	def IdentModeActive(self):
		"""Ident mode is active."""
		pass

	def MotorStandby(self):
		"""Motor stationary."""
		pass

	def BakeActive(self):
		"""Bake mode running"""
		pass

	def TargetVelocityReached(self):
		"""Set when the motor is at target velocity"""
		pass

	def Error(self):
		"""Error flags"""
		pass

	def Status(self):
		"""status flags"""
		pass

	def OperationParameters(self):
		"""Device configuration options."""
		pass

	def ResponseFlag(self):
		"""Error and status flags"""
		pass

	def portIsOpen(self):
		"""Get the value indicating the open or closed status of the serial port"""
		pass

	def portName(self):
		"""Get the name port used for the serial communication"""
		pass

	def portBaud(self):
		"""Get the serial baud rate"""
		pass

	def Connect(self):
		"""Connect in emulation mode"""
		pass

	def Disconnect(self):
		"""Close serial port"""
		pass

	def StepDir(self):
		"""Step and direction."""
		pass

	def StepDirTrigg(self):
		"""Step and direction triggered velocity."""
		pass

	def Remote(self):
		"""USB remote control."""
		pass

	def Joystick(self):
		"""Joystick."""
		pass

	def Bake(self):
		"""Bake."""
		pass

	def Home(self):
		"""Home."""
		pass

	def Jsmode(self):
		"""Joystick operation mode."""
		pass

	def SingleStep(self):
		"""Single step mode."""
		pass

	def Continuous(self):
		"""Continuous mode."""
		pass

	def Tsel(self):
		"""Temperature sensor."""
		pass

	def Thermocouple(self):
		"""Thermocouple K type sensor."""
		pass

	def RTD(self):
		"""RTD sensor."""
		pass

	def NormalOperation(self):
		"""Normal operation."""
		pass

	def CoilShortedLS(self):
		"""Phase shorted to ground."""
		pass

	def Res(self):
		"""Motor microstep resolutions."""
		pass

	def MicroStep8(self):
		"""Microstep resolution 8."""
		pass

	def MicroStep16(self):
		"""Microstep resolution 16."""
		pass

	def MicroStep32(self):
		"""Microstep resolution 32."""
		pass

	def MicroStep64(self):
		"""Microstep resolution 64."""
		pass

	def MicroStep128(self):
		"""Microstep resolution 128."""
		pass

	def MicroStep256(self):
		"""Microstep resolution 256."""
		pass

	def Polarity(self):
		"""Limits activation logic level"""
		pass

	def ActiveHigh(self):
		"""Limit is active when logic level is high."""
		pass

	def ActiveLow(self):
		"""Limit is active when logic level is low."""
		pass

	def StopMode(self):
		"""Behaviour when a limit is triggered."""
		pass

	def HardStop(self):
		"""The motor will stop immediately on a limit being triggered."""
		pass

	def SoftStop(self):
		"""The motor decelerates according to the profile."""
		pass

	def Edge(self):
		"""Edge of the step impulse"""
		pass

	def Rising(self):
		"""A step occurs only on the rising edge."""
		pass

	def Both(self):
		"""a step occurs on both rising and falling edges."""
		pass

	def Interp(self):
		"""Step interpolation."""
		pass

	def Normal(self):
		"""Each step input will cause one step at the current resolution."""
		pass

	def Interp256Microstep(self):
		"""Each step input will be interpolated to 256 microsteps."""
		pass

class SMD4:
	def Enable(self):
		"""Gets or sets the enable state of the limits"""
		pass

	def UsePsignal(self):
		"""Gets or set the enable state of the P signal. If disabled, the P signal is ignored"""
		pass

	def UseQsignal(self):
		"""Get or set the enable state of the Q signal. If disabled, the Q signal is ignored"""
		pass

	def Swap(self):
		"""Get or set the swap state of the limits. The standard configuration is for the P limit to be positioned at the end of the scale 
            reached by the encoder count incrementing, and the Q limit the end of the scale reached by the encoder count decrementing"""
		pass

	def StopMode(self):
		"""Gets or sets the stop mode"""
		pass

	def Behaviour(self):
		"""Gets or sets the behaviour of the subfunction"""
		pass

	def NumberOfOfIterations(self):
		"""Get or set the maximum number of consecutive moves endpoint correction will make to correct the position. If the target position
            cannot be achieved within this number of moves, then the device will enter a warning or fault state according to"""
		pass

	def Tolerance(self):
		"""Get or set the target position tolerance in the current units. This sets the threshold at which a correction will be made; if target and actual position deviate
            by more than this value then endpoint correction will make additional moves to attempt to minimise the error. This must be set in consideration of the resolution of 
            your mechanism."""
		pass

	def ErrorGuard(self):
		"""Get or set a value indicating whether to enable error guard. When enabled, EPC will trigger a warning or error
            when it detects positive feedback is occurring, i.e. corrections are increasing rather than decreasing the error. This
            typically happens when flip is incorrectly set, or the motor spins in the opposite direction than expected.
            This would otherwise result in a runaway escalation of error with each move."""
		pass

	def ValueOne(self):
		"""Gets or set the first guard value in the current units. This is typically the lower limit of the desired range of motion."""
		pass

	def ValueTwo(self):
		"""Gets or set the second guard value in the current units. This is typically the upper limit of the desired range of motion."""
		pass

	def Value(self):
		"""Gets or set the nudge value in the current units"""
		pass

	def PositiveDirection(self):
		"""Nudge the motor in the positve direction by the nudge amount"""
		pass

	def NegativeDirection(self):
		"""Nudge the motor in the negative direction by the nudge amount"""
		pass

	def Clear(self):
		"""Clear the hardware outbound messaging message queue. You should always call this method after beginning coms with the hardwarw"""
		pass

	def GetMessage(self):
		"""Takes one message from the outbound message queue fifo"""
		pass

	def EnableForJoystickAndSdeTriggered(self):
		"""Gets or set a value indicating whether the function should be enabled when using joystick or SDE triggered modes"""
		pass

	def Batch(self):
		"""Batch number"""
		pass

	def Serial(self):
		"""Board serial number within batch"""
		pass

	def IsDefault(self):
		"""Return true if the serial number matches the default pattern"""
		pass

	def Descriptor(self):
		"""Gets an object representing a path to connecting the device"""
		pass

	def Connect(self):
		"""Connect on the default connection which is USB"""
		pass

	def Text(self):
		"""Specify text protocol"""
		pass

	def AutoProtocol(self):
		"""Auto-detect the protocol. This will slow down the connection process as each protocol must be tested in turn"""
		pass

	def IpAddress(self):
		"""Target IP address"""
		pass

	def TcpPortNumber(self):
		"""Port number to use for TCP/IP. Leave null to auto-select based on protocol selection"""
		pass

	def Interface(self):
		"""Interface type, for example USB or Ethernet"""
		pass

	def Protocol(self):
		"""Protocol type, for example Text or Modbus"""
		pass

	def SerialNumber(self):
		"""Target serial number"""
		pass

	def BaudRate(self):
		"""Baud rate, applicable to serial interface only"""
		pass

	def SlaveAddress(self):
		"""Slave address. Only applicable to modbus over USB or Serial."""
		pass

	def IncrementalPqLimits(self):
		"""Incremental encoder PQ limits functionality"""
		pass

	def BoardSerialNumber(self):
		"""Gets the board serial number"""
		pass

	def Readout(self):
		"""Get the last readout from the encoder"""
		pass

	def ReadoutRaw(self):
		"""Get the last readout from the encoder (just the raw counts, which can be read even when encoder selection is none)"""
		pass

	def OffsetPosition(self):
		"""Gets or set an offset value in the current units. This can be used to align the encoder to an arbitary point, for example on a rotary encoder 
            set the 0 readout to align with the zero of your mechanism."""
		pass

	def OffsetPositionRelative(self):
		"""Gets or sets an offset value in the current units. Applied on top of"""
		pass

	def OffsetSpeed(self):
		"""Gets or sets a an offset value in the current units to allow the speed readout to be arbitrarily offset"""
		pass

	def OffsetSpeedRelative(self):
		"""Gets or sets a an offset value in the current units to allow the relative speed readout to be arbitratily offset"""
		pass

	def FirmwareVersion(self):
		"""Get the firmware version"""
		pass

	def Online(self):
		"""Gets a value indicating whether or not the encoder is online"""
		pass

	def Selection(self):
		"""Gets or sets the type of encoder in use"""
		pass

	def UseIncrementalSignalE(self):
		"""Gets or sets a value indicating whether the "E" (Error) signal should be used"""
		pass

	def DisplacementPerCount(self):
		"""Gets or sets the displacement per count, in the current units"""
		pass

	def Flip(self):
		"""Gets or sets a value indicating whether the encoder readout should be flipped/inverted, such that positive is negative and vice versa"""
		pass

	def IncrementalResetZ(self):
		"""Resets the incremental encoder Z counter"""
		pass

	def FlipAutoset(self):
		"""Runs a short self test cycle to determine encoder flip sign, and ensure that EPC will work without positive feedback developing"""
		pass

	def DisplacementSet(self):
		"""Displacements expressed in the current units"""
		pass

	def MechPreset(self):
		"""Mechanism presets"""
		pass

	def TemperatureSensorShorted(self):
		"""Selected temperature sensor is short-circuited"""
		pass

	def TemperatureSensorOpen(self):
		"""Selected temperature sensor is open circuit"""
		pass

	def MotorOverTemperature(self):
		"""Selected temperature sensor is reporting temperature > 190 °C."""
		pass

	def MotorShort(self):
		"""Motor phase to phase or phase to ground short has been detected"""
		pass

	def ExternalInhibit(self):
		"""Motor disabled via external input"""
		pass

	def EmergencyStop(self):
		"""Motor disabled via software"""
		pass

	def ConfigurationError(self):
		"""Configuration data is corrupt"""
		pass

	def SDRAM(self):
		"""SDRAM error"""
		pass

	def MotionControlSubfunctionFault(self):
		"""Motion control subfunction fault"""
		pass

	def JoystickConnected(self):
		"""Joystick is connected"""
		pass

	def LimitNegative(self):
		"""Limit negative input is active"""
		pass

	def LimitPositive(self):
		"""Limit positive input is active"""
		pass

	def ExternalEnable(self):
		"""External enable input state"""
		pass

	def IdentModeActive(self):
		"""Ident mode is active"""
		pass

	def EndpointCorrectionActivity(self):
		"""Endpoint correction activity indicator. Remains on during and for a short time after endpoint correction makes adjustments"""
		pass

	def RangeOfMotionLimiterActivity(self):
		"""Range of motion limiter activity indicator. Turns on when the limiter takes action, and clears when normal operation resumes."""
		pass

	def MotorStationary(self):
		"""Motor stationary"""
		pass

	def BakeActive(self):
		"""Bake mode running"""
		pass

	def TargetVelocityReached(self):
		"""Set when the motor is at target velocity"""
		pass

	def GuardActivity(self):
		"""Guard activity indicator. Turns on when the guard function takes action, and clears when normal operation resumes."""
		pass

	def BoostOperational(self):
		"""Boost Operational"""
		pass

	def BoostDisableJumperFitted(self):
		"""Boost disable jumper is fitted"""
		pass

	def BoostUVLO(self):
		"""Boost Under Voltage Lockout was or is active; this happens when input voltage falls below 48 V. Clear faults to clear this flag."""
		pass

	def OutboundMessageWaiting(self):
		"""There are one or more outbound messages in the hardware waiting to be read"""
		pass

	def MotionControlSubfunctionWarning(self):
		"""Motion control subfunction warning"""
		pass

	def EndpointCorrection(self):
		"""Endpoint correction API. Use an encoder to correct for positioning errors. Positioning is first completed open loop, then
            the encoder is used to adjust the final position to reduce error within a tolerance you specify."""
		pass

	def RangeOfMotionLimiter(self):
		"""Range of motion limiter API. Allows virtual limits to be configured, restricting the range of motion and preventing accidental travel
            outside a prescribed range. Can be used open loop (without an encoder) or closed loop (with an encoder)."""
		pass

	def MotionGuard(self):
		"""Motion guard API. Raises a warning or fault if motion outside prescribed limits occurs. Unlike"""
		pass

	def Nudge(self):
		"""Nudge API. Control and configure a relative displacement that can be triggered by a command or other source such as the joystick"""
		pass

	def DisplacementPerStep(self):
		"""Gets or sets the displacement per step of the mechanism in the current units. This must be configured correctly
            for units other than steps to read correctly. This figure is given as "resolution" in the documentation for AML mechanisms."""
		pass

	def MechanismPreset(self):
		"""Gets or sets the selected mechanism preset. Note that get will always return a dummy preset entry, 'None', and set will apply
            the chosen preset immediately. This is because having applied a preset, the user is free to make further changes to the configuration
            which may mean that it is no longer true to say that the last selected preset applies. Having chosen a preset and made any further changes
            use the save function to commit your changes to the device."""
		pass

	def ZeroAbsoluteAndRelative(self):
		"""Zero absolute and relative counters in a way that is compatible with the encoder and motion control functionality"""
		pass

	def ZeroAbsolute(self):
		"""Zero absolute counters in a way that is compatible with the encoder and motion control functionality"""
		pass

	def ZeroRelative(self):
		"""Zero relative counters in a way that is compatible with the encoder and motion control functionality"""
		pass

	def JoystickPins(self):
		"""Gets a value representing the state of the joystick pins at the microcontroller pins"""
		pass

	def SdelfioPins(self):
		"""Gets a value representing the state of the step, direction, enable, limits and fault signals at the microcontroller pins"""
		pass

	def SdramTest(self):
		"""Test the SDRAM, locks up the SMD4 for a few seconds while running."""
		pass

	def ProductSerialNumber(self):
		"""Get or set the product serial number. This is the serial the customer sees, as distinct from the"""
		pass

	def TemperatureFast(self):
		"""Set a value indicating whether the normal temperature sensor averaging period should be overidden.
            Normally averaging period is about 10 seconds, this cuts that to nothing so that faults and temperature changes register immediately."""
		pass

	def Uuid(self):
		"""Get or set the UUID."""
		pass

	def QspiFlashErase(self):
		"""Erase QSPI flash."""
		pass

	def BoardTestPassFlag(self):
		"""Gets or sets a flag recording board test pass fail status of the board"""
		pass

	def PostSoakTestPassFlag(self):
		"""Gets or sets a flag recording post soak test pass fail status of the board"""
		pass

	def IntegrationTestPassFlag(self):
		"""Gets or sets a flag recording integration test pass fail status of the board"""
		pass

	def ThermocoupleSampleInterval(self):
		"""Gets or sets a value representing the thermocouple sample interval in ms. 
            The firmware always restores the default value on restart so the effect of this is temporary."""
		pass

	def StorePrivate(self):
		"""Store private data that is either inaccessible or read only to the user, such as the serial number"""
		pass

	def EncoderBoardSerialNumber(self):
		"""Encoder board serial number read and write"""
		pass

	def EncoderStoreInternal(self):
		"""Store the encoder board internal settings on the encoder board itself"""
		pass

	def Args(self):
		"""Data returned, less the flags"""
		pass

	def ComsInterface(self):
		"""Coms connection interface type"""
		pass

	def USB(self):
		"""Connected via USB Port"""
		pass

	def COM(self):
		"""Connected via COM Port"""
		pass

	def Ethernet(self):
		"""Connected via Ethernet Port"""
		pass

	def EncoderFlag(self):
		"""Encoder status flags"""
		pass

	def Installed(self):
		"""Encoder module is installed"""
		pass

	def AbsoluteEncoderStatusBit(self):
		"""Absolute encoder status bit"""
		pass

	def CRC(self):
		"""CRC error"""
		pass

	def WARN(self):
		"""Warning"""
		pass

	def ERROR(self):
		"""Error"""
		pass

	def IncrementalEncoderFlag(self):
		"""Incremental encoder signal"""
		pass

	def P(self):
		"""P limit signal"""
		pass

	def Q(self):
		"""Q limit signal"""
		pass

	def E(self):
		"""Error signal"""
		pass

	def MotionControlSubfunctionBehaviourOption(self):
		"""Subfunction behaviour"""
		pass

	def Warning(self):
		"""Subfunction raises a warning on failure. Normal behaviour resumes on next move."""
		pass

	def Fault(self):
		"""Subfunction raises a fault on failure. Clear faults required before normal function resumes."""
		pass

	def EncoderType(self):
		"""Encoder type"""
		pass

	def Incremental(self):
		"""Incremental"""
		pass

	def Absolute(self):
		"""Absolute"""
		pass

	def JoystickMode(self):
		"""Joystick operation mode"""
		pass

	def Single_Step(self):
		"""Single step"""
		pass

	def Continuous(self):
		"""Continuous"""
		pass

	def TemperatureSensorType(self):
		"""Temperature sensor"""
		pass

	def Thermocouple(self):
		"""K-Type Thermocouple"""
		pass

	def RTD(self):
		"""PT100 RTD"""
		pass

	def Freewheel(self):
		"""Freewheel mode"""
		pass

	def Normal_Operation(self):
		"""Normal"""
		pass

	def CoilShortedLS(self):
		"""Phase shorted to ground"""
		pass

	def MicrostepResolution(self):
		"""Microstep resolution"""
		pass

	def MicroStep_8(self):
		"""Microstep resolution 8"""
		pass

	def MicroStep_16(self):
		"""Microstep resolution 16"""
		pass

	def MicroStep_32(self):
		"""Microstep resolution 32"""
		pass

	def MicroStep_64(self):
		"""Microstep resolution 64"""
		pass

	def MicroStep_128(self):
		"""Microstep resolution 128"""
		pass

	def MicroStep_256(self):
		"""Microstep resolution 256"""
		pass

	def SignalPolarity(self):
		"""Limit input polarity"""
		pass

	def Active_High(self):
		"""Limit is active when logic level is high"""
		pass

	def Active_Low(self):
		"""Limit is active when logic level is low"""
		pass

	def LimitStopMode(self):
		"""Behaviour when a limit is triggered"""
		pass

	def Hard_Stop(self):
		"""The motor will stop immediately on a limit being triggered"""
		pass

	def Soft_Stop(self):
		"""The motor decelerates according to the profile"""
		pass

	def StepDirectionEdge(self):
		"""Edge on which a step occurs"""
		pass

	def Rising(self):
		"""A step occurs only on the rising edge"""
		pass

	def Both(self):
		"""a step occurs on both rising and falling edges"""
		pass

	def StepDirectionMode(self):
		"""Step direction modes"""
		pass

	def Triggered(self):
		"""Continuous motion is triggered by an edge on the step input; this is akin to how continuous mode works for the joystick"""
		pass

	def SerialMode(self):
		""""""
		pass

	def RS232(self):
		"""RS232 mode"""
		pass

	def RS485(self):
		"""RS485 mode"""
		pass

	def StepInputInterpolationMode(self):
		"""Step interpolation"""
		pass

	def Normal(self):
		"""Each step input will cause one step at the current resolution"""
		pass

	def Interp256Microstep(self):
		"""Each step input is one full step, which is executed as 256 microsteps"""
		pass

	def Mode(self):
		"""Operation mode"""
		pass

	def StepDir(self):
		"""Step and direction."""
		pass

	def Bake(self):
		"""Bake."""
		pass

	def Local(self):
		"""Local."""
		pass

	def Soak(self):
		"""Soak. Run a pre-configured test program used to exercise the product as part of production test"""
		pass

	def B4800(self):
		"""A step occurs only on the rising edge."""
		pass

	def B9600(self):
		"""A step occurs only on the rising edge."""
		pass

	def B14400(self):
		"""A step occurs only on the rising edge."""
		pass

	def B19200(self):
		"""A step occurs only on the rising edge."""
		pass

	def B38400(self):
		"""A step occurs only on the rising edge."""
		pass

	def B57600(self):
		"""A step occurs only on the rising edge."""
		pass

	def B115200(self):
		"""A step occurs only on the rising edge."""
		pass

	def B230400(self):
		"""A step occurs only on the rising edge."""
		pass

	def B460800(self):
		"""A step occurs only on the rising edge."""
		pass

	def B921600(self):
		"""A step occurs only on the rising edge."""
		pass

	def MeasuementUnits(self):
		"""Units"""
		pass

	def UNIT_STEP(self):
		"""step"""
		pass

	def UNIT_METER(self):
		"""meter"""
		pass

	def UNIT_INCH(self):
		"""inch"""
		pass

	def UNIT_MILLIMETER(self):
		"""millimetre"""
		pass

	def UNIT_MICRON(self):
		"""micron"""
		pass

	def UNIT_DEGREE(self):
		"""degree"""
		pass

	def UNIT_RADIAN(self):
		"""radian"""
		pass

	def UNIT_REVOLUTION(self):
		"""revolution"""
		pass

	def OM_MSG_NONE(self):
		"""No messages"""
		pass

	def OM_MSG_OVERFLOW(self):
		"""Hardware message queue overflow"""
		pass

	def OM_MSG_INTCHANGE_ENCODER_FLIP(self):
		"""Hardware has changed the encoder flip setting"""
		pass

	def Direction(self):
		"""Motor direction"""
		pass

	def ModbusFunctionCode(self):
		"""Modbus function code"""
		pass

	def FC01(self):
		"""Read Coil Status"""
		pass

	def FC02(self):
		"""Read Input Status"""
		pass

	def FC03(self):
		"""Read Holding Registers"""
		pass

	def FC04(self):
		"""Read Input Registers"""
		pass

	def FC05(self):
		"""Force Single Coil"""
		pass

	def FC06(self):
		"""Preset Single Register"""
		pass

	def FC15(self):
		"""Force Multiple Coils"""
		pass

	def FC16(self):
		"""Preset Multiple Registers"""
		pass

	def ComsProtocol(self):
		"""Device comunication Protocols"""
		pass

	def Modbus(self):
		"""Modbus RTU for serial or TCP for ethernet"""
		pass

	def AutoDetect(self):
		"""Unspecified, protocol will be auto-detected"""
		pass

	def ProfileItem(self):
		"""Object defining a pair of values returned by the device when a profile parameter is requested.
            The user value is the value that the user set. The rear value is the same value after conversion by the device
            to the closest actual value that can be set."""
		pass

	def Encoder(self):
		"""Encoder configuration"""
		pass

	def MotionControl(self):
		"""Advanced motion control configuration"""
		pass

	def OutboundMessaging(self):
		"""Mechanisms for the hardware to notify that it has made a change (such as to a property or setting) under its own direction"""
		pass

	def Disconnect(self):
		"""Disconnect the device"""
		pass

	def DeviceName(self):
		"""Gets or sets the device name for the SMD4"""
		pass

	def Acceleration(self):
		"""Gets or sets the acceleration, in the current units per second per second"""
		pass

	def AccelerationDetails(self):
		"""Gets an object representing the configured property value and the actual property value as measured at the motor. Becuase the drive generates step frequencies
            by division of a reference clock, small errors can result between the configured value and the exact value that you get. This is most obvious when
            low step divisions/resoultions are used. The error is typically very small, less than 0.2 Hz with 256x microstepping. 
            If this is relevant to your application, then this command may be used to establish precise values."""
		pass

	def AccelerationCurrent(self):
		"""Gets or sets the motor current applied during acceleration or deceleration"""
		pass

	def ActualPosition(self):
		"""Gets or sets the actual position in the current units. Avoid setting position using this property when using encoders as it may have unexpected side effects. 
            Instead, prefer the 'Zero' methods provided in"""
		pass

	def ActualStepFrequency(self):
		"""Get the live step frequency of the motor in the current units per second"""
		pass

	def BakeElapsed(self):
		"""Gets the elapsed bake time."""
		pass

	def BakeTemperature(self):
		"""Gets or sets the bake temperature setpoint"""
		pass

	def DelayPerCurrentReductionStep(self):
		"""Gets or sets the delay in seconds per current reduction step that occurs when run current is reduced to hold current. 
            Non-zero values result in a smooth reduction in current which reduces the chance of a jerk upon power down.       
            The range is 0 to 0.328 seconds, with a resolution of 4 bits or approx. 20 ms. 
            Current setting has a resolution of 5 bits, or 32 steps, and consequently the current reduction process will only have
            as many steps as exist between the configured run and hold current.
            See also"""
		pass

	def Deceleration(self):
		"""Gets or sets the deceleration in the current units per second per second"""
		pass

	def DecelerationDetails(self):
		"""Gets an object representing the configured property value and the actual property value as measured at the motor. Becuase the drive generates step frequencies
            by division of a reference clock, small errors can result between the configured value and the exact value that you get. This is most obvious when
            low step divisions/resoultions are used. The error is typically very small, less than 0.2 Hz with 256x microstepping. 
            If this is relevant to your application, then this command may be used to establish precise values."""
		pass

	def Flags(self):
		"""Gets the device flags, indicating useful status and error conditions"""
		pass

	def HoldCurrent(self):
		"""Gets or sets the motor hold current.
            Set this as low as possible while still obtaining the required holding torque to minimise temperature rise.
            See also"""
		pass

	def Identify(self):
		"""Gets or sets a value indicating whether the identify function is enabled.F
            When set to true, the green status light on the front of the product flashes.
            This can be used to help identify one device amongst several."""
		pass

	def JoystickEnable(self):
		"""Gets or sets whether the joystick input is enabled. Must be set to true to use the joystick."""
		pass

	def LimitNegativeEnable(self):
		"""Gets or sets the negative limit (corresponding to decrementing step counter) enable."""
		pass

	def LimitNegativePolarity(self):
		"""Gets or sets the negative limit polarity"""
		pass

	def LimitPositiveEnable(self):
		"""Gets or sets the positive limit (corresponding to incrementing step counter) enable."""
		pass

	def LimitPositivePolarity(self):
		"""Gets or sets the negative limit polarity"""
		pass

	def LimitsEnable(self):
		"""Gets or sets global limit enable state.
            If this setting is false, limits are disabled regardless of the state of any other limits configuration item.
            This does not affect other limits configuration settings, allowing limits to be configured as desired, then globally enabled or disabled if required."""
		pass

	def LimitsStopMode(self):
		"""Gets or sets the limits stop mode, which determines behaviour on limit being triggered."""
		pass

	def TransitionToMicrostep(self):
		"""Gets or sets the full step / microstepping transition. When frequency falls below this threshold (approximately), the motor
            switches from full step to the selected microstep resolution. The product determines the upper threshold automatically and
            applies hysteresis to avoid possible jitter between the two stepping modes. The upper threshold cannot be adjusted."""
		pass

	def TransitionToMicrostepDetails(self):
		"""Gets an object representing the configured property value and the actual property value as measured at the motor. Becuase the drive generates step frequencies
            by division of a reference clock, small errors can result between the configured value and the exact value that you get. This is most obvious when
            low step divisions/resoultions are used. The error is typically very small, less than 0.2 Hz with 256x microstepping. 
            If this is relevant to your application, then this command may be used to establish precise values."""
		pass

	def MotorTemperature(self):
		"""Get the motor temperature in °C"""
		pass

	def PowerdownDelay(self):
		"""Gets or sets the delay time in seconds between stand still occurring and the motor current being reduced from the acceleration current to the hold current.
            The range is 0 to 5.5 seconds, with approximately 8 bit / 20 ms resolution
            See also"""
		pass

	def RelativePosition(self):
		"""Gets or sets the relative position counter in steps"""
		pass

	def Resolution(self):
		"""Gets or sets the micro step resolution.Micro stepping is used to smooth motor movement 
            and reduce resonances. Full stepping is always used above a specified threshold step rate, see also"""
		pass

	def RunCurrent(self):
		"""Gets or sets the motor run current. See also"""
		pass

	def MotorTemperatureSensorType(self):
		"""Gets or sets the motor temperature sensor type"""
		pass

	def StartFrequency(self):
		"""Get the start frequency in the current units per second. Must be set less than or equal to"""
		pass

	def StartFrequencyDetails(self):
		"""Gets an object representing the configured property value and the actual property value as measured at the motor. Becuase the drive generates step frequencies
            by division of a reference clock, small errors can result between the configured value and the exact value that you get. This is most obvious when
            low step divisions/resoultions are used. The error is typically very small, less than 0.2 Hz with 256x microstepping. 
            If this is relevant to your application, then this command may be used to establish precise values."""
		pass

	def StepEdge(self):
		"""Gets or sets which edge(s) a step occurs on when in step direction mode"""
		pass

	def Uptime(self):
		"""Gets the total operating time since last reset."""
		pass

	def Units(self):
		"""Gets or sets the measurement units used."""
		pass

	def SerialTermination(self):
		"""Gets or sets a value indicating whether RS485 line termination should be used.If enabled, a 120 ohm termination resistance is placed between the RS485 A and B pins."""
		pass

	def TurnaroundDelay(self):
		"""Gets or sets a value in milliseconds specifying the delay to execute between receipt of a command from the host and the client (SMD4) sending the response. Applicable to RS485 mode only."""
		pass

	def StepFrequency(self):
		"""Gets or sets the target step frequency in the current units per second.
            This is the maximum speed the motor will be run at. The target frequency will only be reached 
            if there is enough time or distance to do so; if moving for a short time, for example, the 
            motor may only accelerate to some fraction of the target frequency before it is time to decelerate to a stop."""
		pass

	def StepFrequencyDetails(self):
		"""Gets an object representing the configured property value and the actual property value as measured at the motor. Becuase the drive generates step frequencies
            by division of a reference clock, small errors can result between the configured value and the exact value that you get. This is most obvious when
            low step divisions/resoultions are used. The error is typically very small, less than 0.2 Hz with 256x microstepping. 
            If this is relevant to your application, then this command may be used to establish precise values."""
		pass

	def StepInterpolation(self):
		"""Gets or sets a value indicating whether the step input should be interpolated to 256 microsteps. Applicable in"""
		pass

	def StopFrequency(self):
		"""Set the stop frequency in the current units per second. Must be greater than or equal to"""
		pass

	def StopFrequencyDetails(self):
		"""Gets an object representing the configured property value and the actual property value as measured at the motor. Becuase the drive generates step frequencies
            by division of a reference clock, small errors can result between the configured value and the exact value that you get. This is most obvious when
            low step divisions/resoultions are used. The error is typically very small, less than 0.2 Hz with 256x microstepping. 
            If this is relevant to your application, then this command may be used to establish precise values."""
		pass

	def UseExternalEnable(self):
		"""Gets or sets a value indicating whether the external enable signal should be respected.
            If not using the external enable and it remains disconnected, set to false"""
		pass

	def ZerowaitTime(self):
		"""Gets or sets the waiting time after ramping down to a stop before the next movement or direction inversion can start.
            Can be used to avoid excess acceleration, e.g. from"""
		pass

	def BoostEnable(self):
		"""Gets or sets a value indicating whether the boost supply should be enabled. The boost supply steps up the input voltage from 
            48 V to 67 V to maximise motor dynamic performance. Enable for best performance.
            Regardless of this setting, the boost supply is disabled when input voltage falls below 48 V, or the boost enable jumper is not fitted.  
            See"""
		pass

	def SerialComsMode(self):
		"""Gets or sets the serial coms mode, either RS232 or RS485. Unplug from the host device before changing the mode"""
		pass

	def GetProtocol(self):
		"""Gets the coms protocol being used on the current interface"""
		pass

	def EthernetLinkUp(self):
		"""Gets a value indicating whether the ethernet interface link is up"""
		pass

	def DHCP(self):
		"""Gets or sets a value indicating whether DHCP is enabled"""
		pass

	def IP(self):
		"""Gets or sets the Ethernet IP Address"""
		pass

	def SubnetMask(self):
		"""Gets or sets the Ethernet Netmask"""
		pass

	def Gateway(self):
		"""Gets or sets the gateway address. When DHCP is enabled, the value read back will be the value assigned by 
            DHCP rather than any value you might have set. 
            Any value set however is retained, and will apply if DHCP is disabled at a later time."""
		pass

	def MAC(self):
		"""Gets the Ethernet interface MAC address"""
		pass

	def JoystickIsConnected(self):
		"""Gets a value indicating whether the joystick is connected.
            Note this wraps the"""
		pass

	def LimitNegativeInputActivate(self):
		"""Gets a value indicating whether limit negative input is active.
            Note this wraps the"""
		pass

	def LimitPositiveInputActive(self):
		"""Gets a value indicating whether limit positive input is active.
            Note this wraps the"""
		pass

	def ExternalEnableInputActive(self):
		"""Gets a value indicating the external enable input state"""
		pass

	def MotorIsStationary(self):
		"""Gets a value indicating whether the motor has come to a stop and is now stationary"""
		pass

	def BakeInProgress(self):
		"""Gets a value indicating whether bake is in progress"""
		pass

	def TemperatureSensorShortCircuitError(self):
		"""Gets a value indicating whether the motor temperature sensor is short circuited"""
		pass

	def TemperatureSensorOpenCircuitError(self):
		"""Gets a value indicating whether the motor temperature sensor is open circuit"""
		pass

	def MotorOverTemperatureError(self):
		"""Gets a value indicating whether the motor temperature has exceeded safe limits, and the motor has been disabled as a result"""
		pass

	def MotorShortCircuitError(self):
		"""Gets a value indicating whether the motor is experiencing a short circuit error"""
		pass

	def ExternalInhibitDisablingDrive(self):
		"""Gets a value indicating whether the drive is disabled on account of the external enable input"""
		pass

	def BoostUVLOError(self):
		"""Gets a value indicating whether the boost circuit is or was disabled due to UVLO (Under-Voltage Lockout)
            When the inut voltage falls significantly below 48 V, the boost circuit is disabled automatically, and re-enabled when input voltage returns to normal.
            The flag is latching, so that short undervoltage events can be captured. Check"""
		pass

	def IsEmergencyStopped(self):
		"""Gets a value indicating whether the device is in emergency stop state"""
		pass

	def FactoryReset(self):
		"""Load factory default configuration. Run the"""
		pass

	def Load(self):
		"""Load the last saved configuration"""
		pass

	def MoveClockwise(self):
		"""Start continuous rotation clockwise. Step count increases"""
		pass

	def MoveCounterClockwise(self):
		"""Start continuous rotation counter-clockwise. Step count decreases"""
		pass

	def QuickStop(self):
		"""Decelerates the motor to a stop within 1 second, disregarding the current profile to do so"""
		pass

	def StartBake(self):
		"""Start bake. Configure the bake temperature setpoint using"""
		pass

	def Stop(self):
		"""Stop the motor, decelerating according to the current profile"""
		pass

	def Store(self):
		"""Store the configuration so that it is preserved on power off"""
		pass

	def Reset(self):
		"""Restart the board, equivelent to powering off and on again"""
		pass

	def ResetToBootloader(self):
		"""Reset the board to the bootloader, preparing it for programming"""
		pass



import clr
clr.AddReference(r"\src\SMD3API.dll")
clr.AddReference(r"\src\SMD4Api.dll")

from Aml.Equipment.SMD4Api import SMD4
from SMD3API import SMD3
from Aml.Equipment.SMD4Api.Protocol import *