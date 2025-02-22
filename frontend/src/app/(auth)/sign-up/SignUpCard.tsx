import {
    Card,
    CardContent,
    CardDescription,
    CardFooter,
    CardHeader,
    CardTitle,
} from "@/components/ui/card";
import SignUpForm from "./SignUpForm";

const SignUpCard = () => {
    return (
        <Card>
            <CardHeader>
                <CardTitle>Join Our Community</CardTitle>
                <CardDescription>
                    Sign up today to get access to the latest blog posts,
                    exclusive content, and join discussion with like-minded
                    readers&#33;
                </CardDescription>
            </CardHeader>
            <CardContent>
                <SignUpForm />
            </CardContent>
            <CardFooter>
                <h1 className="text-center">Social Authentication</h1>
            </CardFooter>
        </Card>
    );
};

export default SignUpCard;
