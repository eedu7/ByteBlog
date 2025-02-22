import {
    Card,
    CardContent,
    CardDescription,
    CardFooter,
    CardHeader,
    CardTitle,
} from "@/components/ui/card";
import SignUpForm from "./SignUpForm";

const SignUpFormCard = () => {
    return (
        <Card>
            <CardHeader>
                <CardTitle>Create an Account</CardTitle>
                <CardDescription>
                    Sign up to access exclusive features and content.
                </CardDescription>
            </CardHeader>
            <CardContent>
                <SignUpForm />
            </CardContent>
            <CardFooter>
                {/* 
                Adding social authentication
                 */}
            </CardFooter>
        </Card>
    );
};

export default SignUpFormCard;
