from __future__ import annotations
from typing import Self, Sequence, Union, TypeAlias, TYPE_CHECKING
if TYPE_CHECKING:
    from _typeshed import FileDescriptorOrPath
BitSequence: TypeAlias = Sequence[Union["0", "1"]]
class BitString:
    """
    BitString
    ---------
    ----------
    A String of bits (0's and 1's).

    ----------
    Input:
    ------
    - bits:
      -----
        - A Sequence (tuple, list, range) of 0's and 1's.
        - Sequence[Union["0", "1"]]
    ----------
    Output:
    -------
    - A String of bits.
    - Functions to turn a String of bits to diffrent data types.
    """
    def __init__(self, bits: BitSequence) -> None:
        self.bitstr = ''.join(bits)
        pass
    def __repr__(self) -> Self:
        return BitString(self.bitstr).bitstr
    def ConvertToInt(self, signed: bool = False) -> int:
        """
        ConvertToInt
        ------------
        ----------
        Convert Bits to an intiger value.

        ----------
        Input:
        ------
        - signed:
          -------
            - Tells whether the output integer is signed.
            - Boolean

        ----------
        Output:
        -------
        - An Intiger value.
        """
        if signed:
            if self.bitstr[0] == "1":
                return int(self.bitstr[1:-1], 2) * -1
            return int(self.bitstr[1:-1], 2)
        return int(self.bitstr, 2)
    def ConvertToBytes(self) -> bytes:
        """
        ConvertToBytes
        --------------
        ----------
        Convert Bits to bytes.

        ----------
        Input:
        ------
        - None

        ----------
        Output:
        -------
        - Bytes
        """
        return bytes(int(self.bitstr[i : i + 8], 2) for i in range(0, len(self.bitstr), 8))
    def ConvertToStr(self, encoding: str = "UTF-8") -> str:
        """
        ConvertToStr
        ------------
        ----------
        Convert the bits to a string using the encoding method.

        ----------
        Input:
        ------
        - encoding:
          ---------
            - The Encoding method used in the binary string.
            - String

        ----------
        Output:
        -------
        - String with the encoding type specified.
        """
        return str(self.ConvertToBytes(), encoding)
class readfrom:
    """
    readfrom
    --------
    ----------
    Read Bits from an object.

    ----------
    This class does not have input types, only subclasses.

    ----------
    All subclasses in this class output a BitString (check BitString for more info).
    """
    class file:
        """
        file
        ----
        ----------
        Read bits from a file.

        ----------
        Input:
        ------
        - file:
          -----
            - The full file path to the file.
            - FileDescriptorOrPath

        ----------
        Output:
        -------
        - BitString (check BitString for more info).
        """
        def __init__(self, file: FileDescriptorOrPath) -> None:
            with open(file, 'rb') as f:
                _bytes = f.read()
            self.bitlist = list(''.join(f'{z:08b}' for z in _bytes))
            pass
        def __repr__(self) -> BitString:
            return BitString(self.bitlist)
        def readbits(self, offset: int, amount: int) -> BitString:
            """
            readbits
            --------
            ----------
            Read an amount of bits from a file.

            ----------
            Input:
            ------
            - offset:
              -------
                - The offset number at which to start reading bytes from the file.
                - Intiger
            - amount:
              -------
                - The amount of bytes to start reading from the offset.
                - Intiger
            
            ----------
            Output:
            -------
            - BitString (check BitString for more info).
            """
            return BitString(self.bitlist[offset:offset+amount])
    class bytes:
        """
        bytes
        -----
        ----------
        Read bits from a bytes.

        ----------
        Input:
        ------
        - _bytes:
          -------
            - The bytes to read.
            - bytes

        ----------
        Output:
        -------
        - BitString (check BitString for more info).
        """
        def __init__(self, _bytes: bytes) -> None:
            self.bitlist = list(''.join(f'{z:08b}' for z in _bytes))
            pass
        def __repr__(self) -> BitString:
            return BitString(self.bitlist)
        def readbits(self, offset: int, amount: int) -> BitString:
            """
            readbits
            --------
            ----------
            Read an amount of bits from bytes.

            ----------
            Input:
            ------
            - offset:
              -------
                - The offset number at which to start reading bytes from the bytes.
                - Intiger
            - amount:
              -------
                - The amount of bytes to start reading from the offset.
                - Intiger
            
            ----------
            Output:
            -------
            - BitString (check BitString for more info).
            """
            return BitString(self.bitlist[offset:offset+amount])
#TODO: Add writeto clsss
#class writeto:
#    class file:
#        def __init__(self, file: FileDescriptorOrPath):
#            self.fileread = open(file)
#            pass
